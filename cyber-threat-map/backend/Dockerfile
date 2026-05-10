# Docker образ для бэкенда Django приложения Карты Киберугроз
# Использует Python 3.11 в качестве базового образа

FROM python:3.11-slim  # Базовый образ с Python 3.11 (slim версия для уменьшения размера)

# Устанавливаем переменную окружения для предотвращения создания .pyc файлов
ENV PYTHONDONTWRITEBYTECODE=1

# Устанавливаем переменную окружения для буферизации вывода Python (важно для логирования в Docker)
ENV PYTHONUNBUFFERED=1

# Создаем директорию для приложения внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости необходимые для работы приложения
RUN apt-get update && apt-get install -y \
    gcc \  # Компилятор для установки пакетов с C расширениями
    libpq-dev \  # Библиотеки PostgreSQL для psycopg2
    curl \  # Утилита для HTTP запросов
    && rm -rf /var/lib/apt/lists/*  # Очищаем кэш apt для уменьшения размера образа

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем Python зависимости из requirements.txt
# --no-cache-dir предотвращает кэширование pip для уменьшения размера
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . .

# Создаем пользователя для запуска приложения от непривилегированного пользователя
# Это улучшает безопасность контейнера
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# Переключаемся на созданного пользователя
USER appuser

# Открываем порт 8000 для доступа к Django серверу
EXPOSE 8000

# Определяем команду для запуска приложения
# Используем gunicorn как production WSGI сервер
# --bind 0.0.0.0:8000 - слушать все интерфейсы на порту 8000
# --workers 4 - запустить 4 worker процесса
# cyber_threat_map.wsgi:application - точка входа WSGI приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "cyber_threat_map.wsgi:application"]
