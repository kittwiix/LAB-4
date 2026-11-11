# -*- coding: utf-8 -*-
"""Задача 1: генератор случайных нот."""
import random

from generators.checks import check_count

NOTES = ['до', 'ре', 'ми', 'фа', 'соль', 'ля', 'си']


def random_notes(count=1_000_000, rng=None):
    """Генерирую заданное число случайных нот из списка NOTES."""
    check_count(count)
    if rng is None:
        rng = random
    for _ in range(count):
        yield rng.choice(NOTES)


def take(generator, count):
    """Беру первые count значений генератора через next."""
    check_count(count)
    result = []
    for _ in range(count):
        try:
            result.append(next(generator))
        except StopIteration:
            break
    return result
