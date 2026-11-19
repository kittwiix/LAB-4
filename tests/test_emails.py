# -*- coding: utf-8 -*-
"""Тесты проверки и фильтрации email-адресов."""
import pytest

from generators.emails import filter_emails, is_valid_email


@pytest.mark.parametrize('email', [
    'ivan@mail.ru',
    'ivan_petrov@mail.ru',
    'user123@yandex.ru',
    'a_b@c_d.ru',
])
def test_valid_email(email):
    assert is_valid_email(email)


@pytest.mark.parametrize('email', [
    'ivanmail.ru',
    'ivan@mailru',
    'ivan.mail@ru',
    'ivan@mail.',
    '@mail.ru',
    'ivan@.ru',
    'ivan@mail.ru!',
    'ivan @mail.ru',
    'иван@mail.ru',
    'ivan@@mail.ru',
    '',
])
def test_invalid_email(email):
    assert not is_valid_email(email)


def test_email_not_string():
    with pytest.raises(TypeError):
        is_valid_email(123)


def test_filter_keeps_order():
    text = 'ivan@mail.ru bad@mail anna_99@yandex.ru oleg@mail.ru'
    assert filter_emails(text) == ['ivan@mail.ru', 'anna_99@yandex.ru', 'oleg@mail.ru']


def test_filter_sample():
    text = ('ivan_petrov@mail.ru user@mailru anna_99@yandex.ru '
            'bad.mail@ru petrov@mail.ru! oleg@mail.ru')
    assert filter_emails(text) == [
        'ivan_petrov@mail.ru',
        'anna_99@yandex.ru',
        'oleg@mail.ru',
    ]


def test_filter_empty_text():
    assert filter_emails('') == []


def test_filter_not_string():
    with pytest.raises(TypeError):
        filter_emails(['ivan@mail.ru'])
