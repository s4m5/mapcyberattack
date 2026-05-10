/**
 * Хук для управления аутентификацией пользователей
 * Предоставляет контекст для хранения состояния входа и JWT токенов
 */

import React, { createContext, useState, useContext, useEffect } from 'react';  // Импорт хуков React
import axios from 'axios';  // Импорт HTTP клиента для API запросов

// Базовый URL API бэкенда
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Создание контекста аутентификации
const AuthContext = createContext(null);

/**
 * Провайдер контекста аутентификации
 * @param {Object} props - Пропсы компонента
 * @param {React.ReactNode} props.children - Дочерние компоненты
 */
export function AuthProvider({ children }) {
  // Состояние текущего пользователя
  const [user, setUser] = useState(null);
  
  // Состояние загрузки (проверка токена при старте)
  const [loading, setLoading] = useState(true);
  
  // Access токен для авторизации запросов
  const [accessToken, setAccessToken] = useState(
    localStorage.getItem('access_token')
  );
  
  // Refresh токен для обновления access токена
  const [refreshToken, setRefreshToken] = useState(
    localStorage.getItem('refresh_token')
  );

  // Эффект для проверки валидности токена при монтировании
  useEffect(() => {
    checkAuth();
  }, []);

  /**
   * Проверка аутентификации при загрузке приложения
   */
  async function checkAuth() {
    // Если нет токена, завершаем проверку
    if (!accessToken) {
      setLoading(false);
      return;
    }

    try {
      // Настройка заголовка авторизации
      axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
      
      // Запрос данных текущего пользователя
      const response = await axios.get(`${API_URL}/auth/me/`);
      setUser(response.data);
    } catch (error) {
      // Если токен истек, пробуем обновить
      if (error.response?.status === 401 && refreshToken) {
        await refreshAccessToken();
      } else {
        // Ошибка или нет refresh токена - выходим
        logout();
      }
    } finally {
      setLoading(false);
    }
  }

  /**
   * Обновление access токена с помощью refresh токена
   */
  async function refreshAccessToken() {
    try {
      const response = await axios.post(`${API_URL}/auth/refresh/`, {
        refresh: refreshToken,
      });
      
      // Сохраняем новые токены
      const newAccessToken = response.data.access;
      const newRefreshToken = response.data.refresh;
      
      setAccessToken(newAccessToken);
      setRefreshToken(newRefreshToken);
      localStorage.setItem('access_token', newAccessToken);
      localStorage.setItem('refresh_token', newRefreshToken);
      
      // Обновляем заголовок авторизации
      axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
      
      return true;
    } catch (error) {
      console.error('Ошибка обновления токена:', error);
      logout();
      return false;
    }
  }

  /**
   * Вход пользователя по логину и паролю
   * @param {string} username - Имя пользователя или email
   * @param {string} password - Пароль
   * @returns {Promise<boolean>} Успешность входа
   */
  async function login(username, password) {
    try {
      // Определение поля (username или email)
      const loginData = username.includes('@') 
        ? { email: username, password } 
        : { username, password };

      // Запрос на вход
      const response = await axios.post(`${API_URL}/auth/login/`, loginData);
      
      // Извлечение токенов и данных пользователя
      const { access, refresh, user: userData } = response.data;
      
      // Сохранение токенов
      setAccessToken(access);
      setRefreshToken(refresh);
      setUser(userData);
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      // Установка заголовка авторизации
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      return true;
    } catch (error) {
      console.error('Ошибка входа:', error);
      throw error.response?.data || { error: 'Неверный логин или пароль' };
    }
  }

  /**
   * Выход пользователя
   */
  async function logout() {
    try {
      // Отправка запроса на blacklist токена
      if (refreshToken) {
        await axios.post(`${API_URL}/auth/logout/`, { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Ошибка выхода:', error);
    } finally {
      // Очистка состояния независимо от результата
      setUser(null);
      setAccessToken(null);
      setRefreshToken(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete axios.defaults.headers.common['Authorization'];
    }
  }

  /**
   * Регистрация нового пользователя
   * @param {Object} userData - Данные пользователя
   * @param {string} userData.username - Имя пользователя
   * @param {string} userData.email - Email
   * @param {string} userData.password - Пароль
   * @param {string} userData.password_confirm - Подтверждение пароля
   * @returns {Promise<boolean>} Успешность регистрации
   */
  async function register(userData) {
    try {
      const response = await axios.post(`${API_URL}/auth/register/`, userData);
      
      // Автоматический вход после регистрации
      const { access, refresh, user: newUser } = response.data;
      
      setAccessToken(access);
      setRefreshToken(refresh);
      setUser(newUser);
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      return true;
    } catch (error) {
      console.error('Ошибка регистрации:', error);
      throw error.response?.data || { error: 'Ошибка регистрации' };
    }
  }

  // Значение контекста для предоставления дочерним компонентам
  const value = {
    user,              // Текущий пользователь
    loading,           // Флаг загрузки
    isAuthenticated: !!user,  // Флаг аутентификации
    login,             // Функция входа
    logout,            // Функция выхода
    register,          // Функция регистрации
    refreshAccessToken,// Функция обновления токена
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Хук для использования контекста аутентификации
 * @returns {Object} Объект с данными и методами аутентификации
 */
export function useAuth() {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth должен использоваться внутри AuthProvider');
  }
  
  return context;
}
