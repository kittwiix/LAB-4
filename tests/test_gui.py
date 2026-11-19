# -*- coding: utf-8 -*-
"""Тесты графического интерфейса на PySide6."""
from generators.gui import MainWindow
from generators.notes import NOTES


def test_main_window_has_four_tabs(qt_app):
    window = MainWindow()
    assert window.tabs.count() == 4
    titles = [window.tabs.tabText(index) for index in range(4)]
    assert titles == [
        'Задача 1: ноты',
        'Задача 2: кратные 3',
        'Задача 3: email',
        'Параллельный замер',
    ]
    window.close()


def test_notes_tab_generates(qt_app):
    window = MainWindow()
    window.notes_tab.count_spin.setValue(5)
    window.notes_tab.generate_button.click()
    lines = window.notes_tab.output.toPlainText().splitlines()
    assert len(lines) == 5
    assert all(note in NOTES for note in lines)
    window.close()


def test_multiples_tab_generates(qt_app):
    window = MainWindow()
    window.multiples_tab.start_spin.setValue(-2)
    window.multiples_tab.count_spin.setValue(3)
    window.multiples_tab.generate_button.click()
    assert window.multiples_tab.output.toPlainText() == '0\n3\n6'
    window.close()


def test_emails_tab_filters(qt_app):
    window = MainWindow()
    window.emails_tab.input_edit.setPlainText('a@mail.ru bad b@mail.ru')
    window.emails_tab.check_button.click()
    assert window.emails_tab.output.toPlainText() == 'a@mail.ru\nb@mail.ru'
    assert window.emails_tab.status.text() == 'Корректных адресов: 2'
    window.close()
