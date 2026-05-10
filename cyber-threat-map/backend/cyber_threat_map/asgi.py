"""
ASGI конфигурация для проекта карты киберугроз.
Используется для асинхронных WebSocket соединений и HTTP запросов.
"""

import os  # Импортируем модуль для работы с переменными окружения

from django.core.asgi import get_asgi_application  # Импортируем функцию для получения ASGI приложения

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
# Это указывает Django какой файл настроек использовать
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_threat_map.settings')

# Получаем стандартное ASGI приложение Django
# Оно будет обрабатывать HTTP запросы
application = get_asgi_application()

# Примечание:
# Для поддержки WebSocket необходимо добавить дополнительные middleware
# и роутинг для channels layers, если требуется реальная WebSocket поддержка
