/**
 * Страница настроек системы
 * Конфигурация параметров мониторинга
 */

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

/**
 * Компонент страницы настроек
 */
function SettingsPage() {
  const { logout } = useAuth();

  function handleLogout() {
    logout();
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-10 bg-gray-900/90 backdrop-blur border-b border-gray-700">
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold text-cyan-400">🛡️ Карта Киберугроз</h1>
            <nav className="flex space-x-4">
              <Link to="/" className="text-gray-400 hover:text-cyan-400 transition-colors">Дашборд</Link>
              <Link to="/attacks" className="text-gray-400 hover:text-cyan-400 transition-colors">Атаки</Link>
              <Link to="/statistics" className="text-gray-400 hover:text-cyan-400 transition-colors">Статистика</Link>
              <a href="/settings" className="text-white hover:text-cyan-400 transition-colors">Настройки</a>
            </nav>
          </div>
          <button onClick={handleLogout} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors">
            Выход
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-20 pb-8 container mx-auto px-4">
        <h2 className="text-2xl font-bold text-white mb-6">⚙️ Настройки системы</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* General Settings */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">📋 Общие настройки</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-gray-300 text-sm mb-2">Интервал обновления (сек)</label>
                <input
                  type="number"
                  defaultValue="5"
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
              <div>
                <label className="block text-gray-300 text-sm mb-2">Максимум атак на карте</label>
                <input
                  type="number"
                  defaultValue="100"
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
            </div>
          </div>

          {/* Firewall Settings */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">🔥 Фаервол</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Мониторинг логов</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" defaultChecked className="sr-only peer" />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-600"></div>
                </label>
              </div>
              <div>
                <label className="block text-gray-300 text-sm mb-2">Путь к логам</label>
                <input
                  type="text"
                  defaultValue="/var/log/syslog"
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
            </div>
          </div>

          {/* GeoIP Settings */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">🌍 GeoIP</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-gray-300 text-sm mb-2">API ключ MaxMind</label>
                <input
                  type="password"
                  placeholder="Введите API ключ"
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
              <button className="w-full py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded transition-colors">
                Обновить базу GeoIP
              </button>
            </div>
          </div>

          {/* Notifications */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">🔔 Уведомления</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Email уведомления</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-600"></div>
                </label>
              </div>
              <div>
                <label className="block text-gray-300 text-sm mb-2">Email для уведомлений</label>
                <input
                  type="email"
                  placeholder="admin@example.com"
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="mt-6 flex justify-end">
          <button className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-semibold rounded-lg transition-all duration-200">
            Сохранить настройки
          </button>
        </div>
      </main>
    </div>
  );
}

export default SettingsPage;
