# -*- coding: utf-8 -*-
"""Задача 2: бесконечный генератор чисел, кратных трём."""
from generators.checks import check_int


def multiples_of_three(start):
    """Выдаю числа, кратные 3, начиная с первого числа не меньше start."""
    check_int(start, 'начало')
    first = start + (-start) % 3
    number = first
    while True:
        yield number
        number += 3
