#!/bin/bash
################################################################################
# Скрипт автоматической установки Интерактивной Карты Киберугроз
# Поддерживает два режима установки:
# 1. Без Docker (прямая установка на сервер)
# 2. С Docker (контейнеризация)
################################################################################

# Цвета для вывода сообщений
RED='\033[0;31m'      # Красный цвет для ошибок
GREEN='\033[0;32m'    # Зеленый цвет для успеха
YELLOW='\033[1;33m'   # Желтый цвет для предупреждений
BLUE='\033[0;34m'     # Синий цвет для информации
NC='\033[0m'          # Сброс цвета

# Переменные конфигурации
PROJECT_DIR="/opt/cyber-threat-map"     # Директория проекта
BACKEND_DIR="${PROJECT_DIR}/backend"    # Директория бэкенда
FRONTEND_DIR="${PROJECT_DIR}/frontend"  # Директория фронтенда
DB_FILE="${BACKEND_DIR}/db.sqlite3"     # Файл базы данных
VENV_DIR="${BACKEND_DIR}/venv"          # Виртуальное окружение Python
ADMIN_USER="admin"                       # Имя пользователя администратора
ADMIN_EMAIL="admin@localhost"           # Email администратора
ADMIN_PASS="CyberThreat2024!"           # Пароль администратора (измените!)

# Функция для вывода цветных сообщений
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Функция для вывода заголовка раздела
print_header() {
    print_message $BLUE "========================================"
    print_message $BLUE "$1"
    print_message $BLUE "========================================"
}

# Функция для проверки наличия команды
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_message $RED "Ошибка: $1 не найден. Пожалуйста, установите $1."
        return 1
    fi
    return 0
}

# Функция для установки зависимостей Debian/Ubuntu
install_debian_deps() {
    print_header "Установка системных зависимостей (Debian/Ubuntu)"
    
    # Обновление списков пакетов
    apt-get update
    
    # Установка необходимых пакетов
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        build-essential \
        libssl-dev \
        libffi-dev \
        git \
        curl \
        wget \
        nginx \
        supervisor \
        geoip-bin \
        libgeoip1 \
        libgeoip-dev \
        sqlite3 \
        logrotate
    
    print_message $GREEN "Системные зависимости установлены успешно"
}

# Функция для установки зависимостей CentOS/RHEL
install_rhel_deps() {
    print_header "Установка системных зависимостей (CentOS/RHEL)"
    
    # Установка EPEL репозитория
    yum install -y epel-release
    
    # Обновление системы
    yum update -y
    
    # Установка необходимых пакетов
    yum install -y \
        python3 \
        python3-pip \
        python3-devel \
        gcc \
        gcc-c++ \
        openssl-devel \
        libffi-devel \
        git \
        curl \
        wget \
        nginx \
        supervisor \
        GeoIP \
        GeoIP-data \
        sqlite \
        logrotate
    
    print_message $GREEN "Системные зависимости установлены успешно"
}

# Функция для настройки виртуального окружения Python
setup_python_venv() {
    print_header "Настройка виртуального окружения Python"
    
    # Создание директории проекта
    mkdir -p ${PROJECT_DIR}
    
    # Создание виртуального окружения
    python3 -m venv ${VENV_DIR}
    
    # Активация виртуального окружения
    source ${VENV_DIR}/bin/activate
    
    # Обновление pip
    pip install --upgrade pip
    
    # Установка зависимостей из requirements.txt
    if [ -f "${BACKEND_DIR}/requirements.txt" ]; then
        pip install -r ${BACKEND_DIR}/requirements.txt
        print_message $GREEN "Python зависимости установлены успешно"
    else
        print_message $RED "Файл requirements.txt не найден"
        return 1
    fi
}

# Функция для настройки базы данных Django
setup_django_db() {
    print_header "Настройка базы данных Django"
    
    # Активация виртуального окружения
    source ${VENV_DIR}/bin/activate
    
    # Переход в директорию бэкенда
    cd ${BACKEND_DIR}
    
    # Применение миграций
    python manage.py migrate
    
    # Сбор статических файлов
    python manage.py collectstatic --noinput
    
    # Создание суперпользователя
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${ADMIN_USER}').exists():
    User.objects.create_superuser(
        username='${ADMIN_USER}',
        email='${ADMIN_EMAIL}',
        password='${ADMIN_PASS}'
    )
    print('Суперпользователь создан успешно')
else:
    print('Суперпользователь уже существует')
EOF
    
    print_message $GREEN "База данных настроена успешно"
}

# Функция для настройки Nginx
setup_nginx() {
    print_header "Настройка веб-сервера Nginx"
    
    # Создание конфигурационного файла Nginx
    cat > /etc/nginx/sites-available/cyber-threat-map << EOF
server {
    listen 80;
    server_name _;
    
    # Директория для статических файлов Django
    location /static/ {
        alias ${BACKEND_DIR}/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Проксирование запросов к Django приложению
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF
    
    # Создание символической ссылки
    ln -sf /etc/nginx/sites-available/cyber-threat-map /etc/nginx/sites-enabled/
    
    # Удаление дефолтной конфигурации
    rm -f /etc/nginx/sites-enabled/default
    
    # Проверка конфигурации Nginx
    nginx -t
    
    # Перезапуск Nginx
    systemctl restart nginx
    systemctl enable nginx
    
    print_message $GREEN "Nginx настроен успешно"
}

# Функция для настройки Supervisor
setup_supervisor() {
    print_header "Настройка Supervisor для управления процессами"
    
    # Создание конфигурационного файла Supervisor
    cat > /etc/supervisor/conf.d/cyber-threat-map.conf << EOF
[program:cyber-threat-map]
command=${VENV_DIR}/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 cyber_threat_map.wsgi:application
directory=${BACKEND_DIR}
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
numprocs=1
redirect_stderr=true
stdout_logfile=/var/log/cyber-threat-map/gunicorn.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
environment=DJANGO_SETTINGS_MODULE="cyber_threat_map.settings"
EOF
    
    # Создание директории для логов
    mkdir -p /var/log/cyber-threat-map
    
    # Обновление конфигурации Supervisor
    supervisorctl reread
    supervisorctl update
    supervisorctl start cyber-threat-map
    
    print_message $GREEN "Supervisor настроен успешно"
}

# Функция для настройки логирования фаервола
setup_firewall_logging() {
    print_header "Настройка логирования фаервола"
    
    # Настройка iptables для логирования
    # Добавляем правило для логирования входящих соединений
    iptables -A INPUT -j LOG --log-prefix "CYBER_THREAT_MAP: " --log-level 4 2>/dev/null || true
    
    # Для ufw включаем логирование
    if command -v ufw &> /dev/null; then
        ufw logging on 2>/dev/null || true
    fi
    
    # Для nftables создаем таблицу логирования
    if command -v nft &> /dev/null; then
        nft add table inet filter 2>/dev/null || true
        nft add chain inet filter input '{ type filter hook input priority 0; policy accept; }' 2>/dev/null || true
        nft add rule inet filter input log prefix \"CYBER_THREAT_MAP: \" 2>/dev/null || true
    fi
    
    # Настройка logrotate для логов приложения
    cat > /etc/logrotate.d/cyber-threat-map << EOF
/var/log/cyber-threat-map/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        supervisorctl restart cyber-threat-map > /dev/null 2>&1 || true
    endscript
}
EOF
    
    print_message $GREEN "Логирование фаервола настроено"
}

# Функция для установки с Docker
setup_docker() {
    print_header "Установка с использованием Docker"
    
    # Проверка наличия Docker
    if ! command -v docker &> /dev/null; then
        print_message $YELLOW "Docker не найден. Установка Docker..."
        curl -fsSL https://get.docker.com | sh
    fi
    
    # Проверка наличия Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_message $YELLOW "Docker Compose не найден. Установка..."
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    # Переход в директорию проекта
    cd ${PROJECT_DIR}
    
    # Сборка и запуск контейнеров
    docker-compose up -d --build
    
    # Применение миграций
    docker-compose exec -T backend python manage.py migrate
    
    # Создание суперпользователя
    docker-compose exec -T backend python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${ADMIN_USER}').exists():
    User.objects.create_superuser('${ADMIN_USER}', '${ADMIN_EMAIL}', '${ADMIN_PASS}')
    print('Суперпользователь создан')
EOF
    
    print_message $GREEN "Docker установка завершена успешно"
}

# Функция для показа итоговой информации
show_final_info() {
    print_header "Установка завершена успешно!"
    
    print_message $GREEN "Приложение доступно по адресу: http://$(hostname -I | awk '{print $1}')"
    print_message $YELLOW "Административная панель: http://$(hostname -I | awk '{print $1}')/admin/"
    print_message $YELLOW "API доступен по адресу: http://$(hostname -I | awk '{print $1}')/api/"
    print_message $WHITE "Логин администратора: ${ADMIN_USER}"
    print_message $WHITE "Пароль администратора: ${ADMIN_PASS}"
    print_message $RED "ВАЖНО: Измените пароль администратора после первого входа!"
    
    print_message $BLUE "Полезные команды:"
    echo "  - Перезапуск приложения: supervisorctl restart cyber-threat-map"
    echo "  - Просмотр логов: tail -f /var/log/cyber-threat-map/gunicorn.log"
    echo "  - Остановка приложения: supervisorctl stop cyber-threat-map"
    echo "  - Статус приложения: supervisorctl status cyber-threat-map"
}

# Основная функция установки без Docker
install_without_docker() {
    print_header "Начало установки (режим без Docker)"
    
    # Определение дистрибутива
    if [ -f /etc/debian_version ]; then
        install_debian_deps
    elif [ -f /etc/redhat-release ]; then
        install_rhel_deps
    else
        print_message $RED "Неподдерживаемый дистрибутив Linux"
        exit 1
    fi
    
    # Настройка Python окружения
    setup_python_venv
    
    # Настройка базы данных
    setup_django_db
    
    # Настройка Nginx
    setup_nginx
    
    # Настройка Supervisor
    setup_supervisor
    
    # Настройка логирования
    setup_firewall_logging
    
    # Показ итоговой информации
    show_final_info
}

# Обработка аргументов командной строки
case "${1:-without-docker}" in
    --docker|-d)
        setup_docker
        ;;
    --without-docker|-w)
        install_without_docker
        ;;
    --help|-h)
        echo "Использование: $0 [--docker|--without-docker|--help]"
        echo "  --docker, -d      Установка с использованием Docker"
        echo "  --without-docker, -w  Установка без Docker (прямая на сервер)"
        echo "  --help, -h        Показать эту справку"
        ;;
    *)
        install_without_docker
        ;;
esac
