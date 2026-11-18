# -*- coding: utf-8 -*-
"""ЛР №4, вариант 10. Генераторы и встроенные функции Python."""
import argparse
import math

from generators.emails import filter_emails
from generators.multiples import multiples_of_three
from generators.notes import random_notes, take
from generators.parallel import run_benchmark

MENU = """
--- Генераторы и встроенные функции: вариант 10 ---
1 - Задача 1: 20 случайных нот из генератора
2 - Задача 2: числа, кратные 3
3 - Задача 3: фильтрация email-адресов
4 - Параллельный замер (Well-done)
0 - Выход
"""

SAMPLE_EMAILS = ('ivan_petrov@mail.ru user@mailru anna_99@yandex.ru '
                 'bad.mail@ru petrov@mail.ru! oleg@mail.ru')


def read_int(prompt, default=None):
    """Читаю целое число; запятую принимаю как десятичный разделитель."""
    while True:
        text = input(prompt).strip().replace(',', '.')
        if not text and default is not None:
            return default
        try:
            value = float(text)
        except ValueError:
            print('Ошибка: нужно целое число')
            continue
        if not math.isfinite(value) or value != int(value):
            print('Ошибка: нужно целое число')
            continue
        return int(value)


def show_notes():
    """Показываю первые 20 нот из генератора на 1 000 000 значений."""
    print('Первые 20 нот из 1 000 000:')
    print(' '.join(take(random_notes(), 20)))


def show_multiples():
    """Спрашиваю начало и показываю первые 20 чисел, кратных трём."""
    start = read_int('Начало поиска (Enter - -100): ', -100)
    print('Числа, кратные 3:')
    print(' '.join(str(number) for number in take(multiples_of_three(start), 20)))


def show_emails():
    """Спрашиваю строку адресов и вывожу только корректные."""
    while True:
        text = input('Адреса через пробел: ').strip()
        if text:
            break
        print('Ошибка: строка не может быть пустой')
    valid = filter_emails(text)
    print('Корректные адреса:')
    print(' '.join(valid) if valid else 'нет')
    print(f'Всего корректных: {len(valid)}')


def show_benchmark():
    """Запускаю замер последовательной и параллельной версии."""
    total = read_int('Сколько адресов (Enter - 1000000): ', 1_000_000)
    workers = read_int('Сколько процессов (Enter - 4): ', 4)
    print('Считаю, это может занять несколько секунд...')
    try:
        result = run_benchmark(total, workers)
    except (TypeError, ValueError) as error:
        print('Ошибка:', error)
        return
    print(result)


def run_console():
    """Главный цикл консольного меню."""
    while True:
        print(MENU)
        choice = input('Выберите пункт: ').strip()
        if choice == '0':
            print('Выход')
            break
        if choice == '1':
            show_notes()
        elif choice == '2':
            show_multiples()
        elif choice == '3':
            show_emails()
        elif choice == '4':
            show_benchmark()
        else:
            print('Нет такого пункта меню')


def run_demo():
    """Показываю готовые примеры без ввода — этот режим запускается в Docker."""
    print('Задача 1. Первые 20 нот из 1 000 000:')
    print(' '.join(take(random_notes(), 20)))
    print()
    print('Задача 2. Числа, кратные 3, начиная с -100:')
    numbers = take(multiples_of_three(-100), 20)
    print(' '.join(str(number) for number in numbers))
    print()
    print('Задача 3. Корректные адреса:')
    valid = filter_emails(SAMPLE_EMAILS)
    print(' '.join(valid))
    print(f'Всего корректных: {len(valid)}')
    print()
    print('Параллельный замер:')
    print(run_benchmark(1_000_000, 4))


def main():
    """Выбираю режим запуска по аргументам командной строки."""
    parser = argparse.ArgumentParser(description='ЛР №4: генераторы Python')
    parser.add_argument('--console', action='store_true', help='консольное меню')
    parser.add_argument('--demo', action='store_true', help='примеры без ввода')
    args = parser.parse_args()
    if args.demo:
        run_demo()
    elif args.console:
        run_console()
    else:
        from generators.gui import run_gui
        run_gui()


if __name__ == '__main__':
    main()
