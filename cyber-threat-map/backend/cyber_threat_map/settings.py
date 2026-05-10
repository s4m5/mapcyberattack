"""
Настройки Django проекта для системы карты киберугроз.
Конфигурация включает базы данных, безопасность, middleware, шаблоны и API.
"""

from pathlib import Path  # Импорт модуля для работы с путями файловых систем
import os  # Импорт модуля для работы с переменными окружения
from datetime import timedelta  # Импорт timedelta для настройки времени жизни JWT токенов

# Построение абсолютного пути к базовой директории проекта (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django для криптографической подписи сессий, токенов и т.д.
# В продакшене должен храниться в переменной окружения для безопасности
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-cyber-threat-map-dev-key-change-in-production')

# Режим отладки: True для разработки, False для продакшена
# Включает подробные страницы ошибок и автоперезагрузку сервера
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Список разрешенных хостов для доступа к сайту
# В продакшене необходимо указать реальные доменные имена
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Приложения Django которые будут использоваться в проекте
INSTALLED_APPS = [
    # Стандартные приложения Django
    'django.contrib.admin',  # Административная панель
    'django.contrib.auth',  # Система аутентификации
    'django.contrib.contenttypes',  # Система типов контента
    'django.contrib.sessions',  # Система сессий
    'django.contrib.messages',  # Система сообщений
    'django.contrib.staticfiles',  # Обработка статических файлов
    
    # Сторонние приложения
    'rest_framework',  # Django REST Framework для создания API
    'rest_framework_simplejwt',  # JWT аутентификация
    'corsheaders',  # Поддержка CORS для доступа с других доменов
    
    # Локальные приложения проекта
    'api',  # Основное приложение с моделями и API карты киберугроз
]

# Middleware - компоненты обрабатывающие запросы и ответы
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Безопасность запросов
    'corsheaders.middleware.CorsMiddleware',  # CORS обработка (должен быть первым)
    'django.contrib.sessions.middleware.SessionMiddleware',  # Управление сессиями
    'django.middleware.common.CommonMiddleware',  # Общие настройки URL
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация пользователей
    'django.contrib.messages.middleware.MessageMiddleware',  # Обработка сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
]

# Корневой URL конфигурации
ROOT_URLCONF = 'cyber_threat_map.urls'

# Настройка шаблонизатора Django для рендеринга HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Движок шаблонов
        'DIRS': [],  # Дополнительные директории шаблонов (пусто для API-only проекта)
        'APP_DIRS': True,  # Искать шаблоны в директориях приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Отладочная информация
                'django.template.context_processors.request',  # Объект request
                'django.contrib.auth.context_processors.auth',  # Данные пользователя
                'django.contrib.messages.context_processors.messages',  # Сообщения
            ],
        },
    },
]

# WSGI приложение для запуска сервера
WSGI_APPLICATION = 'cyber_threat_map.wsgi.application'

# Конфигурация базы данных PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Движок PostgreSQL
        'NAME': os.environ.get('POSTGRES_DB', 'cyber_threat_db'),  # Имя базы данных
        'USER': os.environ.get('POSTGRES_USER', 'cyber_user'),  # Пользователь БД
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'cyber_password'),  # Пароль БД
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),  # Хост БД
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),  # Порт БД
    }
}

# Настройка парольной валидации для безопасности пользователей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['username', 'email'],  # Проверка на схожесть с username/email
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Минимальная длина пароля
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Проверка на распространенные пароли
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Запрет чисто числовых паролей
    },
]

# Язык интерфейса по умолчанию
LANGUAGE_CODE = 'ru-ru'  # Русский язык

# Часовой пояс для отображения времени
TIME_ZONE = 'Europe/Moscow'  # Московское время

# Использование интернационализации
USE_I18N = True  # Включить переводы

# Использование локализации форматов чисел и дат
USE_L10N = True  # Локализованные форматы

# Использование timezone-aware дат и времени
USE_TZ = True  # Датирование с учетом часовых поясов

# Директория для сбора статических файлов (CSS, JS, изображения)
STATIC_URL = '/static/'  # URL для доступа к статике
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Директория для собранной статики

# Тип пользовательской модели (кастомная модель User вместо стандартной)
AUTH_USER_MODEL = 'api.User'

# Настройки Django REST Framework
REST_FRAMEWORK = {
    # Классы аутентификации: JWT токен или базовая авторизация
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT токены
        'rest_framework.authentication.SessionAuthentication',  # Сессионная аутентификация
    ],
    # Разрешения: только авторизованные пользователи
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Пагинация ответов API
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,  # Количество записей на странице
    # Фильтры для поиска и фильтрации данных
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',  # Поиск по тексту
        'rest_framework.filters.OrderingFilter',  # Сортировка
    ],
}

# Настройки JWT токенов для аутентификации
SIMPLE_JWT = {
    # Время жизни access токена (короткоживущий токен для доступа к API)
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    # Время жизни refresh токена (долгоживущий токен для обновления access)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    # Алгоритм подписи токенов
    'ALGORITHM': 'HS256',
    # Ключ для подписи токенов (используется SECRET_KEY)
    'SIGNING_KEY': SECRET_KEY,
    # Разрешить обновление токенов
    'ROTATE_REFRESH_TOKENS': True,
    # Запретить повторное использование refresh токенов
    'BLACKLIST_AFTER_ROTATION': True,
}

# Настройки CORS для доступа с фронтенда
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080'
).split(',')

# Разрешить передачу credentials (cookies, authorization headers) через CORS
CORS_ALLOW_CREDENTIALS = True

# Логгирование - настройка системы логов Django
LOGGING = {
    'version': 1,  # Версия конфигурации логгирования
    'disable_existing_loggers': False,  # Не отключать существующие логгеры
    'formatters': {
        'verbose': {
            # Подробный формат логов с временем, уровнем, модулем и сообщением
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            # Простой формат: уровень и сообщение
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            # Вывод логов в консоль
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'file': {
            # Вывод логов в файл
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
    },
    'root': {
        # Корневой логгер: все логи пишутся в консоль и файл
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            # Логгер Django: наследует handlers от root
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            # Логгер приложения api
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
