# -*- coding: utf-8 -*-
"""Задача 3: отбор корректных email-адресов."""
import re

EMAIL_RE = re.compile(r'[A-Za-z0-9_]+@[A-Za-z0-9_]+\.[A-Za-z0-9_]+')


def is_valid_email(email):
    """Проверяю адрес: разрешены латинские буквы, цифры и _, затем @ и точка."""
    if not isinstance(email, str):
        raise TypeError('адрес должен быть строкой')
    return EMAIL_RE.fullmatch(email) is not None


def filter_emails(text):
    """Оставляю корректные адреса из строки, сохраняя исходный порядок."""
    if not isinstance(text, str):
        raise TypeError('список адресов нужно передать строкой')
    words = text.split()
    return list(filter(is_valid_email, words))
