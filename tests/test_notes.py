# -*- coding: utf-8 -*-
"""Тесты генератора случайных нот."""
import random

import pytest

from generators.notes import NOTES, random_notes, take


def test_notes_count():
    notes = take(random_notes(50), 10)
    assert len(notes) == 10


def test_notes_from_list():
    notes = take(random_notes(100), 20)
    assert all(note in NOTES for note in notes)


def test_notes_reproducible():
    first = take(random_notes(10, random.Random(5)), 10)
    second = take(random_notes(10, random.Random(5)), 10)
    assert first == second


def test_generator_is_lazy():
    generator = random_notes(1_000_000)
    assert iter(generator) is generator
    assert next(generator) in NOTES
    generator.close()


def test_take_stops_at_end():
    assert len(take(random_notes(3), 10)) == 3


@pytest.mark.parametrize('value', [0, -1, -100])
def test_bad_count_value(value):
    with pytest.raises(ValueError):
        list(random_notes(value))


@pytest.mark.parametrize('value', [1.5, float('nan'), float('inf'), True, '5'])
def test_bad_count_type(value):
    with pytest.raises(TypeError):
        list(random_notes(value))
