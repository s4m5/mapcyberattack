# Dockerfile для фронтенда React приложения
# Создает образ с собранным React приложением и Nginx для раздачи статики

# Этап 1: Сборка React приложения
FROM node:18-alpine AS builder

# Установка рабочей директории
WORKDIR /app

# Копирование package файлов для установки зависимостей
COPY package*.json ./

# Установка зависимостей npm
RUN npm ci --only=production

# Копирование исходного кода приложения
COPY . .

# Аргументы сборки для настройки API URL
ARG REACT_APP_API_URL=http://localhost:8000/api
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Сборка React приложения для продакшена
RUN npm run build

# Этап 2: Финальный образ с Nginx
FROM nginx:alpine

# Метаданные образа
LABEL maintainer="Cyber Threat Map Team"
LABEL description="React frontend for Cyber Threat Map"
LABEL version="1.0.0"

# Копирование собранного React приложения в директорию Nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Копирование конфигурации Nginx (будет переопределено через volume)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Удаление дефолтной конфигурации Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Порт на котором слушает Nginx
EXPOSE 80

# Health check для проверки работоспособности
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Команда запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
