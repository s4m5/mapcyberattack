# Интерактивная Карта Киберугроз - Документация Проекта

## 📋 Описание проекта

**Карта Киберугроз** - это система мониторинга и визуализации кибератак в реальном времени с интерактивной 3D картой мира. Проект отображает атаки на ваш сервер, анализирует логи фаервола (iptables/nftables/ufw) и показывает геолокацию источников атак.

### Ключевые возможности

- 🌍 **3D Глобус** с анимацией атак в реальном времени
- 🔴 **Цветовая кодировка** протоколов (TCP=зеленый, UDP=синий, ICMP=красный)
- 📊 **Статистика Top-10**: страны, порты, типы атак, уязвимости
- 🔐 **JWT Аутентификация** пользователей
- 📈 **История атак** с фильтрацией по периодам
- 🔔 **Мониторинг логов** syslog, iptables, nftables, ufw
- 🎨 **Современный UI** на React + Tailwind CSS

---

## 🏗️ Архитектура проекта

```
cyber-threat-map/
├── backend/                 # Django бэкенд
│   ├── cyber_threat_map/    # Настройки проекта
│   │   ├── settings.py      # Конфигурация Django
│   │   ├── urls.py          # URL маршруты
│   │   ├── wsgi.py          # WSGI конфигурация
│   │   └── asgi.py          # ASGI конфигурация
│   ├── api/                 # Основное приложение
│   │   ├── models.py        # Модели данных
│   │   ├── views.py         # API представления
│   │   ├── serializers.py   # DRF сериализаторы
│   │   ├── urls.py          # API маршруты
│   │   ├── admin.py         # Админ панель
│   │   ├── log_parser.py    # Парсер логов
│   │   └── apps.py          # Конфиг приложения
│   ├── manage.py            # Скрипт управления
│   ├── requirements.txt     # Python зависимости
│   └── Dockerfile           # Docker образ
├── frontend/                # React фронтенд
│   ├── src/                 # Исходный код
│   │   ├── components/      # React компоненты
│   │   ├── pages/           # Страницы приложения
│   │   ├── hooks/           # Custom хуки
│   │   ├── utils/           # Утилиты
│   │   └── styles/          # Стили
│   ├── package.json         # npm зависимости
│   └── Dockerfile           # Docker образ
├── docker/                  # Docker конфигурации
│   └── nginx.conf           # Конфиг Nginx
├── scripts/                 # Скрипты установки
│   └── install.sh           # Автоматическая установка
├── docker-compose.yml       # Оркестрация контейнеров
└── docs/                    # Документация
    └── README.md            # Этот файл
```

---

## 🚀 Быстрый старт

### Вариант 1: Установка с Docker (рекомендуется)

```bash
# Переход в директорию проекта
cd /workspace/cyber-threat-map

# Запуск всех сервисов одной командой
docker-compose up -d --build

# Проверка статуса контейнеров
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

**Доступ к приложению:**
- Главная: http://localhost/
- API: http://localhost/api/
- Админ-панель: http://localhost/admin/

**Учетные данные по умолчанию:**
- Логин: `admin`
- Пароль: `CyberThreat2024!`

---

### Вариант 2: Нативная установка (без Docker)

```bash
# Запуск скрипта автоматической установки
cd /workspace/cyber-threat-map
sudo ./scripts/install.sh --without-docker

# Или с параметрами
sudo ./scripts/install.sh --without-docker \
    --admin-user=admin \
    --admin-password=MySecurePassword123
```

**Ручная установка по шагам:**

#### Шаг 1: Установка системных зависимостей

```bash
# Обновление пакетов
sudo apt-get update

# Установка Python, Node.js и других зависимостей
sudo apt-get install -y python3-pip python3-venv python3-dev \
    libpq-dev gcc curl git nodejs npm postgresql redis-server nginx
```

#### Шаг 2: Настройка базы данных PostgreSQL

```bash
# Вход в PostgreSQL
sudo -u postgres psql

# Создание пользователя и базы данных
CREATE USER cyber_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE cyber_threat_db OWNER cyber_user;
GRANT ALL PRIVILEGES ON DATABASE cyber_threat_db TO cyber_user;
\q
```

#### Шаг 3: Настройка бэкенда

```bash
cd /workspace/cyber-threat-map/backend

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Создание файла .env
cat > .env << EOF
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
POSTGRES_DB=cyber_threat_db
POSTGRES_USER=cyber_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
EOF

# Выполнение миграций
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver 0.0.0.0:8000
```

#### Шаг 4: Настройка фронтенда

```bash
cd /workspace/cyber-threat-map/frontend

# Установка зависимостей
npm install --legacy-peer-deps

# Сборка production версии
npm run build

# Копирование статики
sudo cp -r dist/* /usr/share/nginx/html/
```

#### Шаг 5: Настройка Nginx

```bash
# Создание конфигурации
sudo cat > /etc/nginx/sites-available/cyber-threat-map << 'EOF'
server {
    listen 80;
    server_name localhost;
    
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
    }
}
EOF

# Включение сайта
sudo ln -sf /etc/nginx/sites-available/cyber-threat-map /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Перезапуск Nginx
sudo nginx -t && sudo systemctl restart nginx
```

---

## 🔧 Настройка фаервола для логирования

### Для iptables

```bash
# Добавление правила логирования всех входящих соединений
sudo iptables -A INPUT -j LOG --log-prefix "CYBER_THREAT_MAP: " --log-level 4

# Сохранение правил
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

### Для UFW

```bash
# Включение логирования
sudo ufw logging on

# Установка уровня логирования
sudo ufw logging medium
```

### Для nftables

```bash
# Добавление правила логирования
sudo nft add rule inet filter input log prefix \"CYBER_THREAT_MAP: \"
```

### Просмотр логов

```bash
# Журнал systemd
journalctl -f | grep CYBER_THREAT_MAP

# Системный лог
tail -f /var/log/syslog | grep CYBER_THREAT_MAP

# Лог ядра
dmesg | grep CYBER_THREAT_MAP
```

---

## 📡 API Документация

### Аутентификация

#### Регистрация пользователя
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

#### Вход (получение JWT токенов)
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "CyberThreat2024!"
}

# Ответ:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

#### Обновление токена
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Кибератаки

#### Список атак
```http
GET /api/attacks/?limit=50&protocol=TCP&severity=high
Authorization: Bearer <access_token>
```

**Параметры запроса:**
- `limit` - количество записей (по умолчанию 50)
- `protocol` - фильтр по протоколу (TCP, UDP, ICMP)
- `severity` - фильтр по уровню опасности (low, medium, high, critical)
- `start_date` - начальная дата (ISO формат)
- `end_date` - конечная дата
- `search` - поиск по IP, типу атаки, стране

#### Детали атаки
```http
GET /api/attacks/{id}/
Authorization: Bearer <access_token>
```

### Статистика

#### Дашборд статистики
```http
GET /api/dashboard/?hours=24
Authorization: Bearer <access_token>

# Ответ:
{
  "period_hours": 24,
  "total_attacks": 1250,
  "unique_sources": 342,
  "top_countries": [...],
  "top_protocols": [...],
  "top_attack_types": [...]
}
```

#### Геолокация по IP
```http
GET /api/geo/?ip=192.168.1.1
Authorization: Bearer <access_token>
```

---

## 🎨 Компоненты фронтенда

### Структура React приложения

```
frontend/src/
├── App.jsx              # Корневой компонент
├── main.jsx             # Точка входа
├── components/
│   ├── Globe3D.jsx      # 3D глобус (globe.gl)
│   ├── AttackArc.jsx    # Дуги атак
│   ├── StatsPanel.jsx   # Панель статистики
│   ├── AttackList.jsx   # Список атак
│   ├── Header.jsx       # Шапка приложения
│   └── Login.jsx        # Форма входа
├── pages/
│   ├── Dashboard.jsx    # Главная страница
│   ├── Map.jsx          # Страница карты
│   ├── Analytics.jsx    # Аналитика
│   └── Settings.jsx     # Настройки
├── hooks/
│   ├── useAttacks.js    # Хук для получения атак
│   └── useStats.js      # Хук для статистики
├── utils/
│   ├── api.js           # API клиент (axios)
│   └── colors.js        # Цвета протоколов
└── styles/
    └── index.css        # Глобальные стили (Tailwind)
```

### Подключение к API

```javascript
// utils/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для добавления JWT токена
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

---

## 🔒 Безопасность

### Рекомендации для продакшена

1. **Измените секретные ключи:**
   ```bash
   # Генерация нового SECRET_KEY
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Отключите DEBUG режим:**
   ```env
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

3. **Настройте HTTPS:**
   ```nginx
   server {
       listen 443 ssl;
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       # ... остальная конфигурация
   }
   ```

4. **Защитите базу данных:**
   - Используйте сложные пароли
   - Ограничьте доступ по IP
   - Регулярно делайте бэкапы

5. **Обновляйте зависимости:**
   ```bash
   # Бэкенд
   pip list --outdated
   pip install --upgrade <package>
   
   # Фронтенд
   npm outdated
   npm update
   ```

---

## 🐛 Отладка и логи

### Логи бэкенда

```bash
# Docker режим
docker-compose logs backend
docker-compose logs -f backend  # в реальном времени

# Нативный режим
tail -f /workspace/cyber-threat-map/backend/debug.log
journalctl -u cyber-backend -f
```

### Логи фронтенда

```bash
# Браузер консоль (F12)
# или
docker-compose logs frontend
```

### Логи базы данных

```bash
# PostgreSQL логи
sudo tail -f /var/log/postgresql/postgresql-*.log

# Docker
docker-compose logs db
```

---

## 📊 Мониторинг производительности

### Проверка статуса сервисов

```bash
# Docker контейнеры
docker-compose ps
docker stats

# Systemd сервисы
systemctl status cyber-backend
systemctl status cyber-celery
systemctl status nginx

# Использование ресурсов
htop
df -h
free -m
```

### Оптимизация базы данных

```sql
-- Анализ таблиц
ANALYZE cyberattack;

-- Индексы уже созданы в models.py:
-- - timestamp (для сортировки по времени)
-- - source_ip (для поиска по IP)
-- - protocol (для фильтрации)
```

---

## 🆘 Решение проблем

### Частые ошибки

#### Ошибка: "Connection refused to database"
```bash
# Проверьте что PostgreSQL запущен
systemctl status postgresql
# или
docker-compose ps db

# Проверьте credentials в .env
cat backend/.env | grep POSTGRES
```

#### Ошибка: "CORS policy blocked"
```python
# Добавьте домен фронтенда в settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://yourdomain.com",
]
```

#### Ошибка: "ModuleNotFoundError"
```bash
# Переустановите зависимости
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

#### Ошибка: "npm install failed"
```bash
# Очистите кэш npm
npm cache clean --force

# Попробуйте с флагом
npm install --legacy-peer-deps
```

---

## 📝 Лицензия

Проект распространяется под лицензией MIT.

---

## 👥 Авторы

Разработано командой кибербезопасности для мониторинга и визуализации угроз в реальном времени.

---

## 📞 Поддержка

Для вопросов и предложений создавайте Issues в репозитории проекта.
