/**
 * Страница входа в систему
 * Форма аутентификации пользователей
 */

import React, { useState } from 'react';  // Импорт React и хука состояния
import { Link, useNavigate } from 'react-router-dom';  // Компоненты навигации
import { useAuth } from '../hooks/useAuth';  // Хук аутентификации

/**
 * Компонент страницы входа
 * @returns {JSX.Element} Страница входа
 */
function LoginPage() {
  // Навигатор для перенаправления после успешного входа
  const navigate = useNavigate();
  
  // Получаем функцию login из контекста аутентификации
  const { login } = useAuth();
  
  // Состояния формы
  const [username, setUsername] = useState('');  // Имя пользователя или email
  const [password, setPassword] = useState('');  // Пароль
  const [error, setError] = useState('');  // Сообщение об ошибке
  const [isLoading, setIsLoading] = useState(false);  // Флаг загрузки

  /**
   * Обработчик отправки формы
   * @param {Event} e - Событие отправки формы
   */
  async function handleSubmit(e) {
    e.preventDefault();  // Предотвращаем стандартную отправку формы
    
    // Сбрасываем предыдущие ошибки
    setError('');
    setIsLoading(true);  // Включаем режим загрузки

    try {
      // Вызываем функцию входа
      await login(username, password);
      
      // После успешного входа перенаправляем на главную
      navigate('/');
    } catch (err) {
      // При ошибке показываем сообщение
      setError(err.error || 'Неверный логин или пароль');
    } finally {
      // Выключаем режим загрузки
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      {/* Контейнер формы входа */}
      <div className="max-w-md w-full mx-4">
        {/* Заголовок */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-cyan-400 mb-2">
            🛡️ Карта Киберугроз
          </h1>
          <p className="text-gray-400">
            Система мониторинга сетевых атак
          </p>
        </div>

        {/* Форма входа */}
        <div className="bg-gray-800 rounded-lg shadow-2xl p-8 border border-gray-700">
          <h2 className="text-2xl font-semibold text-white mb-6 text-center">
            Вход в систему
          </h2>

          {/* Сообщение об ошибке */}
          {error && (
            <div className="mb-4 p-3 bg-red-900/50 border border-red-500 rounded text-red-400 text-sm">
              ⚠️ {error}
            </div>
          )}

          {/* Форма */}
          <form onSubmit={handleSubmit}>
            {/* Поле ввода имени пользователя/email */}
            <div className="mb-4">
              <label className="block text-gray-300 text-sm font-medium mb-2">
                Имя пользователя или Email
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-colors"
                placeholder="admin"
                required
                disabled={isLoading}
              />
            </div>

            {/* Поле ввода пароля */}
            <div className="mb-6">
              <label className="block text-gray-300 text-sm font-medium mb-2">
                Пароль
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-colors"
                placeholder="••••••••"
                required
                disabled={isLoading}
              />
            </div>

            {/* Кнопка входа */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 px-4 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Вход...
                </span>
              ) : (
                'Войти'
              )}
            </button>
          </form>

          {/* Ссылка на регистрацию */}
          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              Нет учетной записи?{' '}
              <Link to="/register" className="text-cyan-400 hover:text-cyan-300 font-medium">
                Зарегистрироваться
              </Link>
            </p>
          </div>

          {/* Демо credentials */}
          <div className="mt-6 pt-6 border-t border-gray-700">
            <p className="text-gray-500 text-xs text-center">
              Демо доступ: <span className="text-gray-400">admin / CyberThreat2024!</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;  // Экспорт компонента
