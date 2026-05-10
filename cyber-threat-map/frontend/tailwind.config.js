/**
 * Конфигурация Tailwind CSS
 * Определяет кастомные темы и расширения для hi-tech дизайна
 */

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",                    // HTML файл для сканирования классов
    "./src/**/*.{js,jsx}",            // Все JS/JSX файлы в src директории
  ],
  
  theme: {
    extend: {
      // Кастомные цвета в стиле hi-tech
      colors: {
        cyber: {
          dark: '#0a0f1c',            // Очень темный фон
          gray: '#1a1f2e',            // Темно-серый
          blue: '#06b6d4',            // Cyan (основной акцент)
          green: '#10b981',           // Зеленый (успех)
          red: '#ef4444',             // Красный (опасность)
          yellow: '#f59e0b',          // Желтый (предупреждение)
          purple: '#8b5cf6',          // Фиолетовый
        },
      },
      
      // Кастомные анимации
      animation: {
        'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 3s linear infinite',
        'bounce-slow': 'bounce 2s infinite',
      },
      
      // Эффекты свечения
      boxShadow: {
        'glow-cyan': '0 0 20px rgba(6, 182, 212, 0.5)',
        'glow-green': '0 0 20px rgba(16, 185, 129, 0.5)',
        'glow-red': '0 0 20px rgba(239, 68, 68, 0.5)',
        'glow-blue': '0 0 20px rgba(59, 130, 246, 0.5)',
      },
    },
  },
  
  plugins: [],  // Дополнительные плагины (если нужны)
};
