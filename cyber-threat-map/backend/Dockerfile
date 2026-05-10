# Dockerfile для бэкенда Django проекта Интерактивная Карта Киберугроз
# Определяет среду выполнения для Python приложения

# Базовый образ Python 3.11 (легковесный Alpine Linux)
FROM python:3.11-slim

# Метаданные образа
LABEL maintainer="Cyber Threat Map Team"
LABEL description="Django backend for Interactive Cyber Threat Map"
LABEL version="1.0.0"

# Переменные окружения для Python
# PYTHONUNBUFFERED - отключает буферизацию вывода (важно для логирования в Docker)
ENV PYTHONUNBUFFERED=1

# PYTHONDONTWRITEBYTECODE - предотвращает создание .pyc файлов
ENV PYTHONDONTWRITEBYTECODE=1

# PIP_NO_CACHE_DIR - отключает кэш pip для уменьшения размера образа
ENV PIP_NO_CACHE_DIR=1

# PIP_DISABLE_PIP_VERSION_CHECK - отключает проверку версии pip
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Установка системных зависимостей необходимых для сборки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Библиотеки для компиляции Python пакетов
    build-essential \
    # SSL библиотеки для безопасных соединений
    libssl-dev \
    # FFI для вызова функций из C кода
    libffi-dev \
    # PostgreSQL клиентские библиотеки
    libpq-dev \
    # GeoIP библиотеки для определения геолокации по IP
    libgeoip-dev \
    geoip-bin \
    # Утилиты для работы с базой данных
    postgresql-client \
    # curl для health checks
    curl \
    # Очистка кэша apt для уменьшения размера образа
    && rm -rf /var/lib/apt/lists/*

# Копирование файла зависимостей
COPY requirements.txt /app/

# Установка Python зависимостей из requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копирование исходного кода приложения
COPY . /app/

# Создание директорий для логов и статических файлов
RUN mkdir -p /app/logs /app/staticfiles

# Назначение владельца для директорий
RUN chown -R root:root /app

# Порт на котором работает Django приложение
EXPOSE 8000

# Health check для проверки работоспособности приложения
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Команда запуска приложения по умолчанию
# Переопределяется в docker-compose.yml через command
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "cyber_threat_map.wsgi:application"]
