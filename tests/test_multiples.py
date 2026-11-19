# -*- coding: utf-8 -*-
"""Тесты генератора чисел, кратных трём."""
import pytest

from generators.multiples import multiples_of_three
from generators.notes import take

FIRST_TWENTY = [
    -99, -96, -93, -90, -87, -84, -81, -78, -75, -72,
    -69, -66, -63, -60, -57, -54, -51, -48, -45, -42,
]


def test_first_twenty_from_minus_100():
    assert take(multiples_of_three(-100), 20) == FIRST_TWENTY


def test_start_is_multiple():
    assert take(multiples_of_three(9), 3) == [9, 12, 15]


def test_zero_is_first_multiple():
    assert take(multiples_of_three(-2), 3) == [0, 3, 6]


def test_infinite_generator():
    numbers = take(multiples_of_three(0), 100)
    assert len(numbers) == 100
    assert numbers[-1] == 297


@pytest.mark.parametrize('value', [1.0, float('nan'), float('inf'), True, '3', None])
def test_bad_start(value):
    with pytest.raises(TypeError):
        list(multiples_of_three(value))
