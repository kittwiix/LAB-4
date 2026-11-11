# -*- coding: utf-8 -*-
"""Проверки целых чисел, которые использую во всех заданиях."""


def check_int(value, name='значение'):
    """Проверяю, что значение — целое число, и возвращаю его без изменений."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f'{name} должно быть целым числом')
    return value


def check_count(value, name='количество'):
    """Проверяю количество: это целое число, и оно больше нуля."""
    check_int(value, name)
    if value <= 0:
        raise ValueError(f'{name} должно быть больше нуля')
    return value
