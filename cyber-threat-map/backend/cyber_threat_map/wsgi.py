"""
WSGI конфигурация для проекта карты киберугроз.
Используется для запуска Django приложения с Gunicorn или другими WSGI серверами.
"""

import os  # Импортируем модуль для работы с переменными окружения

from django.core.wsgi import get_wsgi_application  # Импортируем функцию получения WSGI приложения

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
# Это указывает Django какой файл настроек использовать
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_threat_map.settings')

# Получаем стандартное WSGI приложение Django
# Оно будет обрабатывать HTTP запросы от веб-сервера
application = get_wsgi_application()
