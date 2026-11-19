# -*- coding: utf-8 -*-
"""Тесты параллельной проверки и замера производительности."""
import pytest

from generators.emails import is_valid_email
from generators.parallel import (BenchmarkResult, count_valid, generated_emails,
                                 run_benchmark, split_counts)


def test_split_counts():
    assert split_counts(1000, 4) == [250, 250, 250, 250]


def test_split_uneven():
    parts = split_counts(10, 3)
    assert sum(parts) == 10
    assert max(parts) - min(parts) == 1


def test_generated_emails_count():
    emails = list(generated_emails(100, 1))
    assert len(emails) == 100
    assert all(email.endswith('@mail.ru') for email in emails)


def test_count_valid_matches_filter():
    emails = list(generated_emails(2000, 3))
    expected = sum(1 for email in emails if is_valid_email(email))
    assert count_valid(2000, 3) == expected


def test_benchmark_small():
    result = run_benchmark(4000, 2)
    assert isinstance(result, BenchmarkResult)
    assert result.total == 4000
    assert result.workers == 2
    assert result.valid > 0
    assert result.sequential_time > 0
    assert result.parallel_time > 0
    assert result.speedup > 0
    assert 'ускорение' in str(result)


def test_benchmark_bad_total():
    with pytest.raises(ValueError):
        run_benchmark(0, 2)


def test_benchmark_bad_workers():
    with pytest.raises(ValueError):
        run_benchmark(100, 0)


def test_benchmark_workers_more_than_total():
    with pytest.raises(ValueError):
        run_benchmark(2, 4)


def test_benchmark_bad_total_type():
    with pytest.raises(TypeError):
        run_benchmark(100.5, 2)
