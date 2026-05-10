/**
 * Компонент защиты маршрутов
 * Перенаправляет неавторизованных пользователей на страницу входа
 */

import React from 'react';  // Импорт React
import { Navigate } from 'react-router-dom';  // Компонент для перенаправления
import { useAuth } from '../hooks/useAuth';  // Хук аутентификации

/**
 * Компонент ProtectedRoute
 * @param {Object} props - Пропсы компонента
 * @param {React.ReactNode} props.children - Дочерние компоненты
 */
function ProtectedRoute({ children }) {
  // Получаем состояние аутентификации из контекста
  const { isAuthenticated, loading } = useAuth();

  // Показываем индикатор загрузки во время проверки токена
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-cyan-400 text-xl">Загрузка...</div>
      </div>
    );
  }

  // Если пользователь не авторизован, перенаправляем на страницу входа
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Если авторизован, рендерим дочерний компонент
  return children;
}

export default ProtectedRoute;  // Экспорт компонента
