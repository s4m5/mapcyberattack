/**
 * Основной компонент приложения Карта Киберугроз
 * Определяет маршруты и структуру приложения
 */

import React from 'react';  // Импорт React
import { Routes, Route, Navigate } from 'react-router-dom';  // Импорт компонентов маршрутизации
import { AuthProvider } from './hooks/useAuth';  // Импорт провайдера аутентификации

// Импорт страниц приложения
import LoginPage from './pages/LoginPage';  // Страница входа
import DashboardPage from './pages/DashboardPage';  // Страница дашборда с картой
import AttacksPage from './pages/AttacksPage';  // Страница списка атак
import StatisticsPage from './pages/StatisticsPage';  // Страница статистики
import SettingsPage from './pages/SettingsPage';  // Страница настроек
import ProtectedRoute from './components/ProtectedRoute';  // Компонент защиты маршрутов

/**
 * Основной компонент приложения
 * @returns {JSX.Element} Приложение с маршрутизацией
 */
function App() {
  return (
    <AuthProvider>  // Провайдер контекста аутентификации для всего приложения
      <div className="app-container">  // Контейнер приложения
        {/* Определение маршрутов */}
        <Routes>
          {/* Публичный маршрут - страница входа */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* Защищенные маршруты - требуют аутентификации */}
          <Route 
            path="/" 
            element={
              <ProtectedRoute>  // Защита маршрута
                <DashboardPage />  // Главная страница с картой
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/attacks" 
            element={
              <ProtectedRoute>
                <AttacksPage />  // Страница списка атак
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/statistics" 
            element={
              <ProtectedRoute>
                <StatisticsPage />  // Страница статистики
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/settings" 
            element={
              <ProtectedRoute>
                <SettingsPage />  // Страница настроек
              </ProtectedRoute>
            } 
          />
          
          {/* Перенаправление неизвестных маршрутов на главную */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;  // Экспорт компонента по умолчанию
