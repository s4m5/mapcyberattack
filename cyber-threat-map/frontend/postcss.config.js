/**
 * Конфигурация PostCSS для обработки CSS
 * Используется для автопрефиксов и Tailwind CSS
 */

export default {
  plugins: {
    tailwindcss: {},      // Плагин Tailwind CSS для обработки утилитарных классов
    autoprefixer: {},     // Плагин для автоматического добавления вендорных префиксов
  },
};
