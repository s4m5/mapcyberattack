#!/bin/bash
# ============================================================================
# Скрипт автоматической установки и настройки проекта "Карта Киберугроз"
# Поддерживает два режима: с Docker и без Docker
# Совместимые ОС: Ubuntu 22.04/24.04 LTS, Debian 11/12
# ============================================================================

set -e  # Выход при любой ошибке в скрипте

# Цвета для вывода сообщений
RED='\033[0;31m'      # Красный цвет для ошибок
GREEN='\033[0;32m'    # Зеленый цвет для успеха
YELLOW='\033[1;33m'   # Желтый цвет для предупреждений
BLUE='\033[0;34m'     # Синий цвет для информации
NC='\033[0m'          # Сброс цвета (Normal Color)

# Пути и переменные
PROJECT_DIR="/workspace/cyber-threat-map"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"
LOG_FILE="${PROJECT_DIR}/install.log"

# Параметры по умолчанию
USE_DOCKER=true
INSTALL_FRONTEND=true
CREATE_SUPERUSER=true
ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@cybermap.local"
ADMIN_PASSWORD="CyberThreat2024!"

# ============================================================================
# Функции для вывода сообщений
# ============================================================================

log() {
    # Вывод сообщения с временной меткой в лог файл
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

info() {
    # Вывод информационного сообщения (синий цвет)
    echo -e "${BLUE}[INFO]${NC} $1"
    log "INFO: $1"
}

success() {
    # Вывод сообщения об успехе (зеленый цвет)
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    log "SUCCESS: $1"
}

warning() {
    # Вывод предупреждения (желтый цвет)
    echo -e "${YELLOW}[WARNING]${NC} $1"
    log "WARNING: $1"
}

error() {
    # Вывод ошибки (красный цвет)
    echo -e "${RED}[ERROR]${NC} $1"
    log "ERROR: $1"
}

# ============================================================================
# Проверка операционной системы
# ============================================================================

check_os() {
    # Проверка совместимости операционной системы
    # Поддерживаются: Ubuntu 22.04/24.04 LTS, Debian 11/12
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        
        info "Обнаружена ОС: $OS $VER"

        case "$OS" in
            "Ubuntu")
                if [[ "$VER" != "22.04" && "$VER" != "24.04" ]]; then
                    error "Несовместимая версия Ubuntu. Требуется 22.04 или 24.04 LTS."
                    error "Ваша версия: $VER"
                    exit 1
                fi
                success "Версия Ubuntu совместима ($VER)"
                ;;
            "Debian GNU/Linux")
                if [[ "$VER" != "11" && "$VER" != "12" ]]; then
                    error "Несовместимая версия Debian. Требуется 11 или 12."
                    error "Ваша версия: $VER"
                    exit 1
                fi
                success "Версия Debian совместима ($VER)"
                ;;
            *)
                error "Неподдерживаемая ОС: $OS"
                error "Проект разработан для Ubuntu 22.04/24.04 или Debian 11/12."
                exit 1
                ;;
        esac
    else
        error "Файл /etc/os-release не найден. Невозможно определить ОС."
        exit 1
    fi
    info "Проверка ОС пройдена успешно."
}

# ============================================================================
# Функции проверки зависимостей
# ============================================================================

check_root() {
    # Проверка прав суперпользователя
    if [ "$EUID" -ne 0 ]; then
        error "Скрипт должен выполняться от root (используйте sudo)"
        exit 1
    fi
    success "Права root подтверждены"
}

check_docker() {
    # Проверка наличия Docker
    if ! command -v docker &> /dev/null; then
        error "Docker не установлен. Установите Docker сначала."
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose не установлен. Установите Docker Compose."
        return 1
    fi
    
    success "Docker и Docker Compose найдены (версия: $(docker --version))"
    return 0
}

check_python() {
    # Проверка наличия Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 не установлен. Установите Python 3.11+"
        return 1
    fi
    
    local version=$(python3 --version | cut -d' ' -f2)
    info "Python версия: $version"
    return 0
}

check_nodejs() {
    # Проверка наличия Node.js
    if ! command -v node &> /dev/null; then
        error "Node.js не установлен. Установите Node.js 20+"
        return 1
    fi
    
    info "Node.js версия: $(node --version)"
    return 0
}

# ============================================================================
# Функции установки зависимостей
# ============================================================================

install_system_packages() {
    # Установка системных пакетов через apt
    info "Обновление списков пакетов..."
    apt-get update -qq
    
    info "Установка системных зависимостей..."
    apt-get install -y -qq \
        python3-pip \
        python3-venv \
        python3-dev \
        libpq-dev \
        gcc \
        curl \
        git \
        wget \
        build-essential \
        nginx \
        supervisor \
        || { error "Не удалось установить системные пакеты"; exit 1; }
    
    success "Системные пакеты установлены"
}

install_docker() {
    # Установка Docker если не установлен
    if check_docker; then
        info "Docker уже установлен, пропускаем установку"
        return 0
    fi
    
    info "Установка Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    
    # Добавляем текущего пользователя в группу docker
    usermod -aG docker $SUDO_USER 2>/dev/null || true
    
    success "Docker установлен"
}

install_nodejs() {
    # Установка Node.js если не установлен
    if command -v node &> /dev/null; then
        info "Node.js уже установлен, пропускаем"
        return 0
    fi
    
    info "Установка Node.js 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
    
    success "Node.js установлен"
}

# ============================================================================
# Функции настройки бэкенда
# ============================================================================

setup_backend_without_docker() {
    info "Настройка бэкенда (без Docker)..."
    
    cd "$BACKEND_DIR"
    
    # Создание виртуального окружения
    info "Создание Python виртуального окружения..."
    python3 -m venv venv
    source venv/bin/activate
    
    # Установка зависимостей
    info "Установка Python зависимостей..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    
    success "Зависимости бэкенда установлены"
    
    # Настройка переменных окружения
    info "Настройка переменных окружения..."
    cat > .env << EOF
DJANGO_SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -hex 32)
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
POSTGRES_DB=cyber_threat_db
POSTGRES_USER=cyber_user
POSTGRES_PASSWORD=cyber_password_$(openssl rand -hex 8)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_URL=redis://localhost:6379/0
EOF
    
    success "Файл .env создан"
}

setup_database() {
    info "Настройка базы данных PostgreSQL..."
    
    # Установка PostgreSQL если не установлен
    if ! command -v psql &> /dev/null; then
        info "Установка PostgreSQL..."
        apt-get install -y -qq postgresql postgresql-contrib
    fi
    
    # Запуск службы PostgreSQL
    systemctl start postgresql
    systemctl enable postgresql
    
    # Создание базы данных и пользователя
    local db_password="cyber_password_$(openssl rand -hex 8)"
    
    sudo -u postgres psql -c "CREATE USER cyber_user WITH PASSWORD '$db_password';" 2>/dev/null || true
    sudo -u postgres psql -c "CREATE DATABASE cyber_threat_db OWNER cyber_user;" 2>/dev/null || true
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cyber_threat_db TO cyber_user;" 2>/dev/null || true
    
    success "База данных PostgreSQL создана"
    
    # Обновление .env файла с паролем БД
    if [ -f "$BACKEND_DIR/.env" ]; then
        sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$db_password/" "$BACKEND_DIR/.env"
    fi
}

setup_redis() {
    info "Настройка Redis..."
    
    # Установка Redis если не установлен
    if ! command -v redis-server &> /dev/null; then
        info "Установка Redis..."
        apt-get install -y -qq redis-server
    fi
    
    # Запуск службы Redis
    systemctl start redis-server
    systemctl enable redis-server
    
    success "Redis настроен и запущен"
}

run_migrations() {
    info "Выполнение миграций Django..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # Применение миграций
    python manage.py migrate
    
    # Сбор статических файлов
    python manage.py collectstatic --noinput
    
    success "Миграции выполнены"
}

create_superuser() {
    if [ "$CREATE_SUPERUSER" = false ]; then
        info "Создание суперпользователя пропущено"
        return 0
    fi
    
    info "Создание суперпользователя..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # Создание суперпользователя через manages.py
    python manage.py shell << EOF
from api.models import User
if not User.objects.filter(username='$ADMIN_USERNAME').exists():
    User.objects.create_superuser(
        username='$ADMIN_USERNAME',
        email='$ADMIN_EMAIL',
        password='$ADMIN_PASSWORD',
        is_staff=True
    )
    print('Суперпользователь создан')
else:
    print('Пользователь уже существует')
EOF
    
    success "Суперпользователь создан (логин: $ADMIN_USERNAME, пароль: $ADMIN_PASSWORD)"
}

# ============================================================================
# Функции настройки фронтенда
# ============================================================================

setup_frontend_without_docker() {
    if [ "$INSTALL_FRONTEND" = false ]; then
        info "Установка фронтенда пропущена"
        return 0
    fi
    
    info "Настройка фронтенда (без Docker)..."
    
    cd "$FRONTEND_DIR"
    
    # Установка зависимостей npm
    info "Установка npm зависимостей..."
    npm install --legacy-peer-deps
    
    # Сборка production версии
    info "Сборка фронтенда..."
    npm run build
    
    success "Фронтенд собран"
    
    # Копирование статики в директорию Nginx
    info "Копирование статики в Nginx..."
    cp -r dist/* /var/www/html/ 2>/dev/null || cp -r dist/* /usr/share/nginx/html/ 2>/dev/null || true
    
    success "Статика скопирована"
}

setup_nginx() {
    info "Настройка Nginx..."
    
    # Создание конфигурации Nginx
    cat > /etc/nginx/sites-available/cyber-threat-map << 'EOF'
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
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
    
    # Включение сайта
    ln -sf /etc/nginx/sites-available/cyber-threat-map /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Проверка конфигурации и перезапуск
    nginx -t && systemctl restart nginx
    
    success "Nginx настроен"
}

# ============================================================================
# Функции для Docker режима
# ============================================================================

deploy_with_docker() {
    info "Развертывание с Docker..."
    
    cd "$PROJECT_DIR"
    
    # Сборка и запуск контейнеров
    info "Сборка Docker образов (может занять время)..."
    docker-compose build --no-cache
    
    info "Запуск контейнеров..."
    docker-compose up -d
    
    # Ожидание готовности сервисов
    info "Ожидание готовности сервисов..."
    sleep 30
    
    # Создание суперпользователя в Docker
    if [ "$CREATE_SUPERUSER" = true ]; then
        info "Создание суперпользователя..."
        docker-compose exec -T backend python manage.py shell << EOF
from api.models import User
if not User.objects.filter(username='$ADMIN_USERNAME').exists():
    User.objects.create_superuser(
        username='$ADMIN_USERNAME',
        email='$ADMIN_EMAIL',
        password='$ADMIN_PASSWORD',
        is_staff=True
    )
    print('Суперпользователь создан')
EOF
        success "Суперпользователь создан"
    fi
    
    success "Docker контейнеры запущены"
}

# ============================================================================
# Функции создания systemd сервисов
# ============================================================================

create_systemd_services() {
    info "Создание systemd сервисов..."
    
    # Сервис для бэкенда
    cat > /etc/systemd/system/cyber-backend.service << EOF
[Unit]
Description=Cyber Threat Map Backend
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=root
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 cyber_threat_map.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    
    # Сервис для Celery worker
    cat > /etc/systemd/system/cyber-celery.service << EOF
[Unit]
Description=Cyber Threat Map Celery Worker
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=root
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/celery -A cyber_threat_map worker --loglevel=info
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    
    # Перезагрузка systemd и запуск сервисов
    systemctl daemon-reload
    systemctl enable cyber-backend cyber-celery
    systemctl start cyber-backend cyber-celery
    
    success "Systemd сервисы созданы и запущены"
}

# ============================================================================
# Функция настройки фаервола
# ============================================================================

configure_firewall() {
    info "Настройка правил фаервола для логирования атак..."
    
    # Проверка наличия iptables
    if ! command -v iptables &> /dev/null; then
        warning "iptables не найден, пропускаем настройку фаервола"
        return 0
    fi
    
    # Сохранение текущих правил
    iptables-save > /root/iptables.backup.$(date +%Y%m%d%H%M%S)
    
    # Добавление правил логирования
    info "Добавление правил логирования входящих соединений..."
    
    # Логирование новых входящих соединений (для демонстрации)
    iptables -A INPUT -m state --state NEW -j LOG --log-prefix "CYBER_THREAT_MAP: " --log-level 4 2>/dev/null || true
    
    # Сохранение правил (если есть persistence)
    if command -v iptables-persistent &> /dev/null; then
        iptables-save > /etc/iptables/rules.v4
        success "Правила iptables сохранены"
    fi
    
    success "Фаервол настроен для логирования"
    
    info "Пример логов:"
    info "  journalctl -f | grep CYBER_THREAT_MAP"
    info "  или /var/log/syslog | grep CYBER_THREAT_MAP"
}

# ============================================================================
# Основная функция установки
# ============================================================================

main() {
    echo "=============================================="
    echo "  Карта Киберугроз - Установка проекта"
    echo "=============================================="
    echo ""
    
    # Парсинг аргументов командной строки
    while [[ $# -gt 0 ]]; do
        case $1 in
            --without-docker)
                USE_DOCKER=false
                shift
                ;;
            --no-frontend)
                INSTALL_FRONTEND=false
                shift
                ;;
            --no-superuser)
                CREATE_SUPERUSER=false
                shift
                ;;
            --admin-user=*)
                ADMIN_USERNAME="${1#*=}"
                shift
                ;;
            --admin-password=*)
                ADMIN_PASSWORD="${1#*=}"
                shift
                ;;
            --help)
                echo "Использование: $0 [опции]"
                echo ""
                echo "Опции:"
                echo "  --without-docker      Установить без Docker (нативная установка)"
                echo "  --no-frontend         Не устанавливать фронтенд"
                echo "  --no-superuser        Не создавать суперпользователя"
                echo "  --admin-user=NAME     Имя суперпользователя (по умолчанию: admin)"
                echo "  --admin-password=PWD  Пароль суперпользователя"
                echo "  --help                Показать эту справку"
                exit 0
                ;;
            *)
                error "Неизвестная опция: $1"
                exit 1
                ;;
        esac
    done
    
    # Проверка прав root
    check_root
    
    # Проверка операционной системы
    check_os
    
    # Логирование начала установки
    log "Начало установки проекта Карта Киберугроз"
    log "Режим Docker: $USE_DOCKER"
    
    if [ "$USE_DOCKER" = true ]; then
        # ========== Установка с Docker ==========
        info "Выбран режим установки с Docker"
        
        # Проверка Docker
        if ! check_docker; then
            install_docker
        fi
        
        # Развертывание
        deploy_with_docker
        
        success "Установка с Docker завершена!"
        
    else
        # ========== Установка без Docker ==========
        info "Выбран режим нативной установки (без Docker)"
        
        # Проверка зависимостей
        check_python || { install_system_packages; }
        check_nodejs || install_nodejs
        
        # Установка системных пакетов
        install_system_packages
        
        # Настройка бэкенда
        setup_backend_without_docker
        
        # Настройка базы данных
        setup_database
        
        # Настройка Redis
        setup_redis
        
        # Выполнение миграций
        run_migrations
        
        # Создание суперпользователя
        create_superuser
        
        # Настройка фронтенда
        setup_frontend_without_docker
        
        # Настройка Nginx
        setup_nginx
        
        # Создание systemd сервисов
        create_systemd_services
        
        # Настройка фаервола
        configure_firewall
        
        success "Нативная установка завершена!"
    fi
    
    # Вывод итоговой информации
    echo ""
    echo "=============================================="
    echo "  Установка завершена успешно!"
    echo "=============================================="
    echo ""
    echo "Доступ к приложению:"
    echo "  - Главная страница: http://localhost/"
    echo "  - API: http://localhost/api/"
    echo "  - Админ-панель: http://localhost/admin/"
    echo ""
    echo "Учетные данные администратора:"
    echo "  Логин: $ADMIN_USERNAME"
    echo "  Пароль: $ADMIN_PASSWORD"
    echo ""
    echo "Логи установки: $LOG_FILE"
    echo ""
    
    if [ "$USE_DOCKER" = true ]; then
        echo "Управление Docker контейнерами:"
        echo "  docker-compose ps              # Статус контейнеров"
        echo "  docker-compose logs -f         # Просмотр логов"
        echo "  docker-compose down            # Остановка"
        echo "  docker-compose restart         # Перезапуск"
    else
        echo "Управление сервисами:"
        echo "  systemctl status cyber-backend # Статус бэкенда"
        echo "  systemctl status cyber-celery  # Статус Celery"
        echo "  systemctl status nginx         # Статус Nginx"
        echo "  journalctl -f                  # Логи системы"
    fi
    echo ""
    
    log "Установка успешно завершена"
}

# Запуск основной функции
main "$@"
