# Dockerfile для фронтенда React приложения
# Многоэтапная сборка для минимизации размера образа

# Этап 1: Сборка приложения
FROM node:20-alpine AS builder  # Используем легкий Alpine образ с Node.js 20

WORKDIR /app  # Рабочая директория внутри контейнера

# Копируем файлы зависимостей
COPY package.json package-lock.json* ./

# Устанавливаем зависимости (кэшируется если package.json не изменился)
RUN npm ci --only=production || npm install --only=production

# Копируем исходный код
COPY . .

# Собираем приложение для продакшена
RUN npm run build

# Этап 2: Сервер Nginx для раздачи статики
FROM nginx:alpine  # Легкий образ Nginx

# Копируем конфигурацию Nginx
COPY ../docker/nginx.conf /etc/nginx/conf.d/default.conf

# Копируем собранное приложение из предыдущего этапа
COPY --from=builder /app/dist /usr/share/nginx/html

# Открываем порт 80 для HTTP
EXPOSE 80

# Запускаем Nginx в foreground режиме
CMD ["nginx", "-g", "daemon off;"]
