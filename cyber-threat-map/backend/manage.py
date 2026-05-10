#!/usr/bin/env python
"""
Скрипт управления проектом Django (manage.py).
Используется для выполнения различных команд Django:
- запуск сервера разработки
- применение миграций
- создание суперпользователя
- сбор статических файлов
и многих других.
"""

import os  # Импортируем модуль для работы с переменными окружения
import sys  # Импортируем модуль для работы с системными параметрами


def main():
    """
    Основная функция скрипта управления.
    Устанавливает настройки Django и запускает выполнение команд.
    """
    # Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
    # Это указывает Django какой файл настроек использовать
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_threat_map.settings')
    
    try:
        # Импортируем функцию для выполнения команд Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Обрабатываем ошибку импорта Django
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что Django установлен и доступен в PYTHONPATH. "
            "Original error: %s" % exc
        ) from exc
    
    # Выполняем команду переданную через командную строку
    # Например: python manage.py runserver
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Вызываем основную функцию если скрипт запущен напрямую
    main()
