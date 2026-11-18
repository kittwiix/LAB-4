# -*- coding: utf-8 -*-
"""Графический интерфейс на PySide6: четыре вкладки с заданиями ЛР № 4."""
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                               QMessageBox, QPlainTextEdit, QPushButton,
                               QSpinBox, QTabWidget, QVBoxLayout, QWidget)

from generators.emails import filter_emails
from generators.multiples import multiples_of_three
from generators.notes import random_notes, take
from generators.parallel import run_benchmark

SAMPLE_EMAILS = ('ivan_petrov@mail.ru user@mailru anna_99@yandex.ru '
                 'bad.mail@ru petrov@mail.ru! oleg@mail.ru')


class NotesTab(QWidget):
    """Вкладка задачи 1: генерирую случайные ноты и показываю их списком."""

    def __init__(self):
        super().__init__()
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 1_000_000)
        self.count_spin.setValue(20)

        self.generate_button = QPushButton('Сгенерировать')
        self.generate_button.clicked.connect(self.generate)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)

        row = QHBoxLayout()
        row.addWidget(QLabel('Сколько нот взять:'))
        row.addWidget(self.count_spin)
        row.addWidget(self.generate_button)
        row.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addWidget(self.output)

    def generate(self):
        """Беру ноты из генератора и вывожу каждую с новой строки."""
        count = self.count_spin.value()
        notes = take(random_notes(count), count)
        self.output.setPlainText('\n'.join(notes))


class MultiplesTab(QWidget):
    """Вкладка задачи 2: показываю числа, кратные трём, начиная с введённого."""

    def __init__(self):
        super().__init__()
        self.start_spin = QSpinBox()
        self.start_spin.setRange(-1_000_000, 1_000_000)
        self.start_spin.setValue(-100)

        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 1000)
        self.count_spin.setValue(20)

        self.generate_button = QPushButton('Показать числа')
        self.generate_button.clicked.connect(self.generate)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)

        row = QHBoxLayout()
        row.addWidget(QLabel('Начало:'))
        row.addWidget(self.start_spin)
        row.addWidget(QLabel('Сколько чисел:'))
        row.addWidget(self.count_spin)
        row.addWidget(self.generate_button)
        row.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addWidget(self.output)

    def generate(self):
        """Беру первые числа из генератора и вывожу их по одному."""
        start = self.start_spin.value()
        count = self.count_spin.value()
        numbers = take(multiples_of_three(start), count)
        self.output.setPlainText('\n'.join(str(number) for number in numbers))


class EmailsTab(QWidget):
    """Вкладка задачи 3: проверяю адреса и показываю только корректные."""

    def __init__(self):
        super().__init__()
        self.input_edit = QPlainTextEdit()
        self.input_edit.setPlainText(SAMPLE_EMAILS)
        self.input_edit.setMaximumHeight(90)

        self.check_button = QPushButton('Проверить адреса')
        self.check_button.clicked.connect(self.check)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.status = QLabel('Введите адреса через пробел')

        row = QHBoxLayout()
        row.addWidget(self.check_button)
        row.addWidget(self.status)
        row.addStretch()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Адреса через пробел:'))
        layout.addWidget(self.input_edit)
        layout.addLayout(row)
        layout.addWidget(self.output)

    def check(self):
        """Отбираю корректные адреса и обновляю счётчик."""
        valid = filter_emails(self.input_edit.toPlainText())
        self.output.setPlainText('\n'.join(valid))
        self.status.setText(f'Корректных адресов: {len(valid)}')


class BenchmarkTab(QWidget):
    """Вкладка Well-done: сравниваю последовательную и параллельную версии."""

    def __init__(self):
        super().__init__()
        self.count_spin = QSpinBox()
        self.count_spin.setRange(10_000, 2_000_000)
        self.count_spin.setSingleStep(100_000)
        self.count_spin.setValue(500_000)

        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 16)
        self.workers_spin.setValue(4)

        self.run_button = QPushButton('Запустить замер')
        self.run_button.clicked.connect(self.run)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.status = QLabel('Замер занимает несколько секунд')

        row = QHBoxLayout()
        row.addWidget(QLabel('Адресов:'))
        row.addWidget(self.count_spin)
        row.addWidget(QLabel('Процессов:'))
        row.addWidget(self.workers_spin)
        row.addWidget(self.run_button)
        row.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addWidget(self.output)
        layout.addWidget(self.status)

    def run(self):
        """Запускаю замер и показываю времена и ускорение."""
        self.run_button.setEnabled(False)
        self.status.setText('Считаю, подождите...')
        QApplication.processEvents()
        try:
            result = run_benchmark(self.count_spin.value(), self.workers_spin.value())
        except (TypeError, ValueError) as error:
            QMessageBox.warning(self, 'Ошибка', str(error))
            self.status.setText('Ошибка')
        else:
            self.output.setPlainText(str(result))
            self.status.setText('Готово')
        finally:
            self.run_button.setEnabled(True)


class MainWindow(QMainWindow):
    """Главное окно: собираю четыре вкладки в QTabWidget."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Лабораторная работа № 4 — генераторы Python')
        self.resize(760, 560)

        self.tabs = QTabWidget()
        self.notes_tab = NotesTab()
        self.multiples_tab = MultiplesTab()
        self.emails_tab = EmailsTab()
        self.benchmark_tab = BenchmarkTab()

        self.tabs.addTab(self.notes_tab, 'Задача 1: ноты')
        self.tabs.addTab(self.multiples_tab, 'Задача 2: кратные 3')
        self.tabs.addTab(self.emails_tab, 'Задача 3: email')
        self.tabs.addTab(self.benchmark_tab, 'Параллельный замер')
        self.setCentralWidget(self.tabs)


def run_gui():
    """Создаю приложение и показываю главное окно."""
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()
