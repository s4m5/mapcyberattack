/**
 * Конфигурация Vite для сборки React приложения
 * Определяет настройки сервера разработки и билда
 */

import { defineConfig } from 'vite';  // Импорт функции конфигурации
import react from '@vitejs/plugin-react';  // Плагин для поддержки React

// Экспорт конфигурации
export default defineConfig({
  plugins: [react()],  // Использование плагина React
  
  // Настройки сервера разработки
  server: {
    port: 3000,  // Порт для dev сервера
    host: true,  // Доступ с любых IP (не только localhost)
    proxy: {
      // Проксирование API запросов на бэкенд
      '/api': {
        target: 'http://localhost:8000',  // URL бэкенда
        changeOrigin: true,  // Изменять заголовок Origin
      },
    },
  },
  
  // Настройки сборки
  build: {
    outDir: 'dist',  // Директория для выходных файлов
    sourcemap: true,  // Генерировать source maps для отладки
    minify: 'terser',  // Минификация кода
    terserOptions: {
      compress: {
        drop_console: true,  // Удалять console.log в продакшене
      },
    },
  },
});
