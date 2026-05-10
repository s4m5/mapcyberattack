"""
WSGI конфигурация для Django проекта.
Точка входа для WSGI-совместимых веб-серверов (Gunicorn, uWSGI, mod_wsgi).
"""

import os  # Импорт модуля для работы с переменными окружения
import sys  # Импорт модуля для работы с системными параметрами

# Добавляем директорию проекта в PYTHONPATH для корректного импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Устанавливаем переменную окружения с настройками Django
# Это необходимо для инициализации Django приложения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyber_threat_map.settings')

# Импортируем WSGI приложение после установки переменной окружения
# Django не может быть инициализирован без DJANGO_SETTINGS_MODULE
from django.core.wsgi import get_wsgi_application

# Создаем WSGI приложение которое будет обрабатывать HTTP запросы
# application - это callable объект который принимает environ и start_response
application = get_wsgi_application()
