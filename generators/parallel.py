# -*- coding: utf-8 -*-
"""Уровень Well-done: параллельная проверка сгенерированных адресов."""
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from string import ascii_lowercase, digits

from generators.checks import check_count, check_int
from generators.emails import is_valid_email

SYMBOLS = ascii_lowercase + digits + '_'


@dataclass
class BenchmarkResult:
    """Результат замера: времена, число корректных адресов и ускорение."""

    total: int
    workers: int
    valid: int
    sequential_time: float
    parallel_time: float
    speedup: float

    def __str__(self):
        return (f'всего адресов: {self.total}, корректных: {self.valid}; '
                f'последовательно: {self.sequential_time:.2f} с, '
                f'параллельно: {self.parallel_time:.2f} с, '
                f'ускорение: {self.speedup:.2f}')


def make_email(rng):
    """Собираю случайный адрес; иногда добавляю запрещённый символ."""
    name = ''.join(rng.choice(SYMBOLS) for _ in range(8))
    if rng.random() < 0.2:
        name += rng.choice('!# ')
    return name + '@mail.ru'


def generated_emails(count, seed=0):
    """Генерирую count адресов с заданным seed для повторяемых замеров."""
    check_count(count)
    check_int(seed, 'начальное значение')
    rng = random.Random(seed)
    for _ in range(count):
        yield make_email(rng)


def count_valid(count, seed=0):
    """Считаю, сколько корректных адресов в сгенерированной пачке."""
    return sum(1 for email in generated_emails(count, seed) if is_valid_email(email))


def split_counts(total, workers):
    """Делю общее количество на workers почти равных частей."""
    check_count(total, 'общее количество')
    check_count(workers, 'число процессов')
    if workers > total:
        raise ValueError('число процессов не может быть больше количества адресов')
    base, extra = divmod(total, workers)
    return [base + (1 if i < extra else 0) for i in range(workers)]


def _count_task(task):
    """Функция для процесса: распаковываю пару и считаю адреса."""
    count, seed = task
    return count_valid(count, seed)


def run_benchmark(total=1_000_000, workers=None):
    """Сравниваю последовательную и параллельную обработку по времени."""
    if workers is None:
        workers = os.cpu_count() or 1
    parts = split_counts(total, workers)
    tasks = list(zip(parts, range(7, 7 + workers)))

    started = time.perf_counter()
    sequential = sum(count_valid(count, seed) for count, seed in tasks)
    sequential_time = time.perf_counter() - started

    started = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        parallel = sum(pool.map(_count_task, tasks))
    parallel_time = time.perf_counter() - started

    speedup = sequential_time / parallel_time if parallel_time > 0 else 0.0
    return BenchmarkResult(total, workers, sequential, sequential_time,
                           parallel_time, speedup)
