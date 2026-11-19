# -*- coding: utf-8 -*-
"""Общая настройка тестов: Qt работает без экрана."""
import os

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope='session')
def qt_app():
    """Создаю одно приложение Qt на все тесты интерфейса."""
    application = QApplication.instance() or QApplication([])
    yield application
