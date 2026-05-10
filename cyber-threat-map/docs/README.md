# Интерактивная Карта Киберугроз

## Описание проекта

Проект представляет собой интерактивную 3D карту киберугроз в реальном времени, отображающую сетевые атаки на вашу организацию. Система анализирует логи фаервола (iptables/nftables/ufw) и системные логи (syslog), извлекает информацию об атаках и визуализирует их на карте мира.

## Основные возможности

- **Реальное время**: Мониторинг атак в режиме реального времени
- **3D Визуализация**: Интерактивная карта с линиями атак разных цветов
- **Анализ логов**: Парсинг syslog, iptables, nftables, ufw логов
- **Геолокация**: Определение страны и города по IP адресу
- **Статистика**: Топ-10 типов атак, уязвимостей, портов и стран
- **Авторизация**: Безопасный доступ к дашборду с аутентификацией
- **История**: Хранение данных в базе данных с возможностью просмотра по периодам
- **API**: REST API для интеграции с другими системами

## Структура проекта

```
cyber-threat-map/
├── backend/                 # Бэкенд на Django
│   ├── cyber_threat_map/   # Основной проект Django
│   │   ├── settings.py     # Настройки проекта
│   │   ├── urls.py         # URL конфигурация
│   │   ├── wsgi.py         # WSGI конфигурация
│   │   └── asgi.py         # ASGI конфигурация
│   ├── api/                # Приложение API
│   │   ├── models.py       # Модели данных
│   │   ├── views.py        # Представления API
│   │   ├── serializers.py  # Сериализаторы DRF
│   │   ├── urls.py         # URL маршруты API
│   │   ├── admin.py        # Административная панель
│   │   └── log_parser.py   # Парсер логов
│   ├── manage.py           # Скрипт управления Django
│   ├── requirements.txt    # Python зависимости
│   └── Dockerfile          # Docker образ бэкенда
├── frontend/               # Фронтенд на React
│   ├── src/               # Исходный код React
│   ├── public/            # Публичные файлы
│   └── Dockerfile         # Docker образ фронтенда
├── docker/                # Docker конфигурации
│   └── nginx.conf         # Конфигурация Nginx
├── scripts/               # Скрипты установки
│   └── install.sh         # Автоматическая установка
├── docs/                  # Документация
│   └── README.md          # Этот файл
└── docker-compose.yml     # Docker Compose конфигурация
```

## Технологии

### Бэкенд
- **Python 3.11** - Язык программирования
- **Django 4.2** - Веб-фреймворк
- **Django REST Framework** - Создание API
- **PostgreSQL/SQLite** - База данных
- **Redis** - Кэширование и WebSocket
- **Gunicorn** - WSGI сервер
- **GeoIP2** - Геолокация по IP

### Фронтенд
- **React 18** - JavaScript библиотека
- **Tailwind CSS** - CSS фреймворк
- **Three.js/D3.js** - 3D визуализация
- **React Router** - Навигация
- **Axios** - HTTP клиент

### Инфраструктура
- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация контейнеров
- **Nginx** - Веб-сервер и прокси
- **Supervisor** - Управление процессами

## Установка

### Вариант 1: Без Docker (прямая установка на сервер)

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd cyber-threat-map

# Запустите скрипт установки
sudo ./scripts/install.sh --without-docker

# Или вручную:
# 1. Установите зависимости
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx supervisor

# 2. Создайте виртуальное окружение
cd backend
python3 -m venv venv
source venv/bin/activate

# 3. Установите Python зависимости
pip install -r requirements.txt

# 4. Примените миграции
python manage.py migrate

# 5. Соберите статические файлы
python manage.py collectstatic --noinput

# 6. Создайте суперпользователя
python manage.py createsuperuser

# 7. Запустите сервер разработки
python manage.py runserver 0.0.0.0:8000
```

### Вариант 2: С Docker (рекомендуется)

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd cyber-threat-map

# Запустите все сервисы
docker-compose up -d --build

# Проверьте статус контейнеров
docker-compose ps

# Просмотрите логи
docker-compose logs -f

# Остановите сервисы
docker-compose down
```

## Настройка фаервола для логирования

### iptables

```bash
# Включить логирование входящих соединений
sudo iptables -A INPUT -j LOG --log-prefix "CYBER_THREAT_MAP: " --log-level 4

# Сохранить правила
sudo iptables-save > /etc/iptables/rules.v4
```

### UFW

```bash
# Включить логирование
sudo ufw logging on

# Установить уровень логирования
sudo ufw logging medium
```

### nftables

```bash
# Создать таблицу и цепочку для логирования
sudo nft add table inet filter
sudo nft add chain inet filter input { type filter hook input priority 0\; policy accept\; }
sudo nft add rule inet filter input log prefix \"CYBER_THREAT_MAP: \"
```

## Доступ к приложению

После установки приложение доступно по адресу:

- **Главная страница**: http://your-server-ip/
- **API**: http://your-server-ip/api/
- **Админ-панель**: http://your-server-ip/admin/

### Учетные данные по умолчанию

- **Логин**: admin
- **Пароль**: CyberThreat2024! (измените после первого входа!)

## API Endpoints

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /api/auth/login/ | Вход пользователя |
| POST | /api/auth/logout/ | Выход пользователя |
| POST | /api/auth/register/ | Регистрация |

### Атаки

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /api/attacks/ | Список всех атак |
| GET | /api/attacks/{id}/ | Детали атаки |
| POST | /api/attacks/ | Создание атаки |
| PUT | /api/attacks/{id}/ | Обновление атаки |
| DELETE | /api/attacks/{id}/ | Удаление атаки |
| GET | /api/attacks/live/ | Атаки в реальном времени |
| GET | /api/attacks/geo/ | Геоданные атак |

### Статистика

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /api/dashboard/stats/ | Статистика дашборда |
| GET | /api/statistics/ | История статистики |

## Полезные команды

### Docker

```bash
# Запуск сервисов
docker-compose up -d

# Остановка сервисов
docker-compose down

# Перезапуск сервисов
docker-compose restart

# Просмотр логов
docker-compose logs -f backend

# Выполнение команд в контейнере
docker-compose exec backend python manage.py shell

# Применение миграций
docker-compose exec backend python manage.py migrate

# Создание суперпользователя
docker-compose exec backend python manage.py createsuperuser
```

### Без Docker

```bash
# Активация виртуального окружения
source venv/bin/activate

# Запуск сервера разработки
python manage.py runserver

# Применение миграций
python manage.py migrate

# Сбор статики
python manage.py collectstatic --noinput

# Запуск мониторинга логов
python manage.py run_monitor

# Тестирование
python manage.py test
```

## Безопасность

### Рекомендации для продакшена

1. **Измените пароль администратора** после первого входа
2. **Настройте SECRET_KEY** в настройках Django
3. **Используйте HTTPS** с SSL сертификатами
4. **Ограничьте ALLOWED_HOSTS** конкретными доменами
5. **Настройте брандмауэр** для ограничения доступа
6. **Регулярно обновляйте** зависимости системы
7. **Включите логирование** и мониторинг
8. **Настройте резервное копирование** базы данных

## Лицензия

Проект распространяется под лицензией MIT.

## Контакты

Для вопросов и предложений обращайтесь к разработчикам проекта.
