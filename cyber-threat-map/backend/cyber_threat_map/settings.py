#!/usr/bin/env python3
"""
Файл настроек Django проекта для карты киберугроз.
Содержит все необходимые конфигурации для работы приложения.
"""

import os
from pathlib import Path
from datetime import timedelta

# Получение абсолютного пути к базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для криптографической подписи сессий и токенов
# В продакшене необходимо заменить на случайную строку
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-cyber-threat-map-key-change-in-production')

# Режим отладки: True для разработки, False для продакшена
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Разрешенные хосты для доступа к приложению
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Приложения Django установленные в проекте
INSTALLED_APPS = [
    'django.contrib.admin',  # Административная панель Django
    'django.contrib.auth',  # Система аутентификации пользователей
    'django.contrib.contenttypes',  # Система типов контента
    'django.contrib.sessions',  # Управление сессиями пользователей
    'django.contrib.messages',  # Система сообщений для пользователей
    'django.contrib.staticfiles',  # Обработка статических файлов
    'rest_framework',  # Django REST Framework для API
    'rest_framework.authtoken',  # Токенная аутентификация
    'corsheaders',  # Поддержка CORS для фронтенда
    'channels',  # Асинхронные WebSocket соединения
    'api',  # Основное приложение карты киберугроз
]

# Промежуточное ПО (middleware) для обработки запросов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Безопасность HTTP запросов
    'corsheaders.middleware.CorsMiddleware',  # Обработка CORS заголовков
    'django.contrib.sessions.middleware.SessionMiddleware',  # Управление сессиями
    'django.middleware.common.CommonMiddleware',  # Общие настройки Django
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация пользователей
    'django.contrib.messages.middleware.MessageMiddleware',  # Обработка сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
]

# Настройка URL корневого модуля
ROOT_URLCONF = 'cyber_threat_map.urls'

# Шаблоны для рендеринга HTML страниц
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Директории с шаблонами
        'APP_DIRS': True,  # Искать шаблоны в директориях приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Отладочная информация
                'django.template.context_processors.request',  # Объект request в контексте
                'django.contrib.auth.context_processors.auth',  # Данные аутентификации
                'django.contrib.messages.context_processors.messages',  # Сообщения
            ],
        },
    },
]

# Конфигурация ASGI для WebSocket соединений
ASGI_APPLICATION = 'cyber_threat_map.asgi.application'

# Настройки базы данных SQLite по умолчанию
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Используем SQLite
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных
    }
}

# Для продакшена рекомендуется использовать PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'cyber_threat_map'),
#         'USER': os.environ.get('DB_USER', 'cyber_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'secure_password'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

# Кастомная модель пользователя
AUTH_USER_MODEL = 'api.User'

# Настройки парольной валидации
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Локализация приложения
LANGUAGE_CODE = 'ru-ru'  # Русский язык
TIME_ZONE = 'UTC'  # Часовой пояс UTC
USE_I18N = True  # Интернационализация включена
USE_TZ = True  # Использование временных зон

# Статические файлы (CSS, JavaScript, изображения)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Директория для сбора статических файлов

# Медиа файлы (загружаемые пользователями)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Токенная аутентификация
        'rest_framework.authentication.SessionAuthentication',  # Сессионная аутентификация
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Требуется аутентификация
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,  # Количество записей на странице
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',  # Фильтрация по полям
        'rest_framework.filters.SearchFilter',  # Поиск по полям
    ],
}

# Настройки CORS для фронтенда
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
).split(',')

# Настройки Channels для WebSocket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Для разработки
        # Для продакшена использовать Redis:
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     'hosts': [('redis', 6379)],
        # },
    },
}

# Логирование приложения
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'cyber_threat_map.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'api': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Настройки для парсинга логов
SYSLOG_FILE = os.environ.get('SYSLOG_FILE', '/var/log/syslog')  # Путь к syslog
FIREWALL_LOG_FILE = os.environ.get('FIREWALL_LOG_FILE', '/var/log/kern.log')  # Путь к логам фаервола
POLL_INTERVAL = int(os.environ.get('POLL_INTERVAL', '5'))  # Интервал опроса логов в секундах

# GeoIP база данных
GEOIP_DB_PATH = os.environ.get('GEOIP_DB_PATH', '/usr/share/geoip/GeoLite2-City.mmdb')

# Цвета для протоколов
PROTOCOL_COLORS = {
    'TCP': '#00ff00',  # Зеленый
    'UDP': '#0000ff',  # Синий
    'ICMP': '#ff0000',  # Красный
    'HTTP': '#ffff00',  # Желтый
    'HTTPS': '#00ffff',  # Голубой
    'SSH': '#ff00ff',  # Маджента
    'FTP': '#ffa500',  # Оранжевый
    'DNS': '#800080',  # Фиолетовый
    'OTHER': '#ffffff',  # Белый
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
