# -*- coding: utf-8 -*-
"""Пакет generators: три задания лабораторной работы № 4."""
from generators.checks import check_count, check_int
from generators.emails import EMAIL_RE, filter_emails, is_valid_email
from generators.multiples import multiples_of_three
from generators.notes import NOTES, random_notes, take
from generators.parallel import BenchmarkResult, run_benchmark

__all__ = [
    'BenchmarkResult',
    'EMAIL_RE',
    'NOTES',
    'check_count',
    'check_int',
    'filter_emails',
    'is_valid_email',
    'multiples_of_three',
    'random_notes',
    'run_benchmark',
    'take',
]
