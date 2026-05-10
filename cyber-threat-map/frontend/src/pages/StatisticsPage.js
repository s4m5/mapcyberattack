/**
 * Страница статистики и аналитики
 * Графики и диаграммы по атакам
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Компонент страницы статистики
 */
function StatisticsPage() {
  const { logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  async function loadStats() {
    try {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      const response = await axios.get(`${API_URL}/dashboard/?hours=168`); // 7 дней
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Ошибка загрузки статистики:', error);
      setLoading(false);
    }
  }

  function handleLogout() {
    logout();
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-cyan-400 text-xl">Загрузка статистики...</div>
      </div>
    );
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
              <a href="/statistics" className="text-white hover:text-cyan-400 transition-colors">Статистика</a>
            </nav>
          </div>
          <button onClick={handleLogout} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors">
            Выход
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-20 pb-8 container mx-auto px-4">
        <h2 className="text-2xl font-bold text-white mb-6">📊 Статистика за 7 дней</h2>

        {/* Summary Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-gray-400 text-sm mb-2">Всего атак</h3>
              <p className="text-3xl font-bold text-cyan-400">{stats.total_attacks}</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-gray-400 text-sm mb-2">Уникальных источников</h3>
              <p className="text-3xl font-bold text-green-400">{stats.unique_sources}</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-gray-400 text-sm mb-2">Протоколов</h3>
              <p className="text-3xl font-bold text-blue-400">{stats.top_protocols?.length || 0}</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-gray-400 text-sm mb-2">Стран</h3>
              <p className="text-3xl font-bold text-purple-400">{stats.top_countries?.length || 0}</p>
            </div>
          </div>
        )}

        {/* Top Lists */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Top Countries */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">🌍 Топ стран</h3>
            <ul className="space-y-2">
              {stats?.top_countries?.slice(0, 10).map((item, idx) => (
                <li key={idx} className="flex justify-between items-center">
                  <span className="text-gray-300">{item.country}</span>
                  <span className="text-cyan-400 font-medium">{item.count}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Top Protocols */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">🔌 Топ протоколов</h3>
            <ul className="space-y-2">
              {stats?.top_protocols?.slice(0, 10).map((item, idx) => (
                <li key={idx} className="flex justify-between items-center">
                  <span className="text-gray-300">{item.protocol}</span>
                  <span className="text-blue-400 font-medium">{item.count}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Top Attack Types */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">⚔️ Топ типов атак</h3>
            <ul className="space-y-2">
              {stats?.top_attack_types?.slice(0, 10).map((item, idx) => (
                <li key={idx} className="flex justify-between items-center">
                  <span className="text-gray-300">{item.attack_type}</span>
                  <span className="text-red-400 font-medium">{item.count}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Severity Distribution */}
        {stats?.severity_distribution && (
          <div className="mt-6 bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">🎯 Распределение по уровням опасности</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {stats.severity_distribution.map((item, idx) => (
                <div key={idx} className="text-center p-4 bg-gray-700/50 rounded">
                  <p className={`text-2xl font-bold ${
                    item.severity === 'critical' ? 'text-red-400' :
                    item.severity === 'high' ? 'text-orange-400' :
                    item.severity === 'medium' ? 'text-yellow-400' :
                    'text-green-400'
                  }`}>
                    {item.count}
                  </p>
                  <p className="text-gray-400 text-sm mt-1">
                    {item.severity === 'critical' ? 'Критический' :
                     item.severity === 'high' ? 'Высокий' :
                     item.severity === 'medium' ? 'Средний' :
                     'Низкий'}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default StatisticsPage;
