#!/usr/bin/env python
"""
Скрипт управления Django проектом для карты киберугроз.
Позволяет запускать сервер, выполнять миграции, создавать суперпользователя и другие операции.
"""

import os
import sys


def main():
    """
    Основная функция запуска Django проекта.
    Устанавливает переменную окружения DJANGO_SETTINGS_MODULE и запускает execute_from_command_line.
    """
    # Устанавливаем переменную окружения с настройками Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_threat_map.settings')
    
    try:
        # Импортируем функцию для выполнения команд Django из командной строки
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Обработка ошибки импорта Django
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что Django установлен и доступен в PYTHONPATH."
        ) from exc
    
    # Выполняем команду Django с переданными аргументами командной строки
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Запускаем основную функцию при выполнении скрипта напрямую
    main()
