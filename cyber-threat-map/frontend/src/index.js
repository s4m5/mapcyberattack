/**
 * Основной файл входа приложения React
 * Инициализирует корневой компонент и подключает стили
 */

import React from 'react';  // Импорт библиотеки React
import ReactDOM from 'react-dom/client';  // Импорт ReactDOM для рендеринга
import { BrowserRouter } from 'react-router-dom';  // Импорт роутера для навигации
import App from './App';  // Импорт основного компонента приложения
import './styles/index.css';  // Импорт глобальных стилей

// Находим корневой элемент DOM для рендеринга
const rootElement = document.getElementById('root');

// Если элемент найден, создаем корень React и рендерим приложение
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);  // Создаем корневой узел React 18+
  
  // Рендерим приложение с оберкой BrowserRouter для маршрутизации
  root.render(
    <React.StrictMode>  // StrictMode для выявления потенциальных проблем
      <BrowserRouter>  // Обертка для клиентской маршрутизации
        <App />  // Основной компонент приложения
      </BrowserRouter>
    </React.StrictMode>
  );
} else {
  // Если элемент не найден, выводим ошибку в консоль
  console.error('Root element not found');
}
