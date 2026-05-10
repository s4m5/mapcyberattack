"""
ASGI конфигурация для Django проекта.
Точка входа для ASGI-совместимых веб-серверов (Daphne, Uvicorn).
Поддерживает асинхронные запросы и WebSocket соединения.
"""

import os  # Импорт модуля для работы с переменными окружения

# Устанавливаем переменную окружения с настройками Django
# Это необходимо для инициализации Django приложения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_threat_map.settings')

# Импортируем ASGI приложение после установки переменной окружения
# Django не может быть инициализирован без DJANGO_SETTINGS_MODULE
from django.core.asgi import get_asgi_application

# Создаем ASGI приложение которое будет обрабатывать асинхронные HTTP запросы
# application - это callable объект для асинхронных серверов
application = get_asgi_application()
