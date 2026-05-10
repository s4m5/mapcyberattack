# 🛡️ Карта Киберугроз - Cyber Threat Map

Интерактивная система мониторинга и визуализации кибератак в реальном времени.

## 📋 Описание

Проект представляет собой полнофункциональное веб-приложение для:
- Мониторинга сетевых атак в реальном времени
- Визуализации атак на 3D глобусе
- Анализа статистики и трендов
- Управления настройками системы

## 🏗️ Архитектура

### Бэкенд (Django + DRF)
- **Django 5.0** - Веб-фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - База данных
- **Redis** - Кэш и брокер сообщений
- **Celery** - Фоновые задачи
- **JWT** - Аутентификация

### Фронтенд (React + Vite)
- **React 18** - UI библиотека
- **Vite** - Сборщик
- **TailwindCSS** - Стилизация
- **Globe.gl** - 3D визуализация
- **React Router** - Маршрутизация

## 🚀 Быстрый старт

### С помощью Docker (рекомендуется)

```bash
# Перейти в директорию проекта
cd /workspace/cyber-threat-map

# Запустить все сервисы
docker-compose up -d

# Создать суперпользователя
docker-compose exec backend python manage.py createsuperuser

# Открыть в браузере
# http://localhost - Фронтенд
# http://localhost:8000/admin - Админка Django
```

### Без Docker (разработка)

#### Бэкенд
```bash
cd backend

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер разработки
python manage.py runserver
```

#### Фронтенд
```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev

# Открыть http://localhost:3000
```

## 📁 Структура проекта

```
cyber-threat-map/
├── backend/                 # Django бэкенд
│   ├── api/                # Основное приложение
│   │   ├── models.py       # Модели данных
│   │   ├── views.py        # API представления
│   │   ├── serializers.py  # Сериализаторы
│   │   ├── urls.py         # URL маршруты
│   │   ├── admin.py        # Админка
│   │   └── log_parser.py   # Парсер логов
│   ├── cyber_threat_map/   # Настройки проекта
│   ├── manage.py           # Скрипт управления
│   └── requirements.txt    # Зависимости Python
├── frontend/               # React фронтенд
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── pages/          # Страницы приложения
│   │   ├── hooks/          # Custom хуки
│   │   ├── utils/          # Утилиты
│   │   ├── styles/         # CSS стили
│   │   ├── App.js          # Корневой компонент
│   │   └── index.js        # Точка входа
│   ├── package.json        # Зависимости Node.js
│   └── vite.config.js      # Конфигурация Vite
├── docker/                 # Docker конфигурации
├── scripts/                # Скрипты установки
├── docker-compose.yml      # Docker Compose
└── README.md              # Документация
```

## 🔌 API Endpoints

### Аутентификация
- `POST /api/auth/register/` - Регистрация
- `POST /api/auth/login/` - Вход
- `POST /api/auth/logout/` - Выход
- `POST /api/auth/refresh/` - Обновление токена
- `GET /api/auth/me/` - Текущий пользователь

### Атаки
- `GET /api/attacks/` - Список атак
- `GET /api/attacks/{id}/` - Детали атаки
- `POST /api/attacks/` - Создание атаки
- `GET /api/live/` - Атаки в реальном времени

### Статистика
- `GET /api/dashboard/` - Статистика дашборда
- `GET /api/statistics/` - Историческая статистика

### Геолокация
- `GET /api/geo/?ip=x.x.x.x` - GeoIP данные

## 🔐 Данные для входа

По умолчанию после установки:
- **Логин:** admin
- **Пароль:** CyberThreat2024!

## 📊 Возможности

- ✅ 3D визуализация атак на глобусе
- ✅ Фильтрация по протоколам, странам, уровням опасности
- ✅ Статистика и аналитика
- ✅ Real-time обновления
- ✅ Адаптивный дизайн
- ✅ JWT аутентификация
- ✅ Парсинг системных логов
- ✅ GeoIP определение

## 🛠️ Технологии

| Компонент | Технология |
|-----------|------------|
| Backend | Python 3.11+, Django 5.0 |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Frontend | React 18, Vite 5 |
| Styling | TailwindCSS 3 |
| Visualization | Globe.gl, Three.js |
| Container | Docker, Docker Compose |

## 📝 Лицензия

MIT License

## 👥 Авторы

Разработано для демонстрации возможностей современного веб-стека.
