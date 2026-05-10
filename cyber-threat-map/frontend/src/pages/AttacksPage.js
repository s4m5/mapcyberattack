/**
 * Страница списка всех атак
 * Таблица с фильтрацией и пагинацией
 */

import React, { useState, useEffect } from 'react';  // Импорт React и хуков
import { Link } from 'react-router-dom';  // Компонент навигации
import { useAuth } from '../hooks/useAuth';  // Хук аутентификации
import axios from 'axios';  // HTTP клиент

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Компонент страницы списка атак
 */
function AttacksPage() {
  const { logout } = useAuth();
  const [attacks, setAttacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    protocol: '',
    severity: '',
    country: '',
  });

  useEffect(() => {
    loadAttacks();
  }, [filters]);

  async function loadAttacks() {
    try {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      const params = new URLSearchParams();
      if (filters.protocol) params.append('protocol', filters.protocol);
      if (filters.severity) params.append('severity', filters.severity);
      if (filters.country) params.append('country', filters.country);

      const response = await axios.get(`${API_URL}/attacks/?${params.toString()}`);
      setAttacks(response.data.results || []);
      setLoading(false);
    } catch (error) {
      console.error('Ошибка загрузки атак:', error);
      setLoading(false);
    }
  }

  function handleLogout() {
    logout();
  }

  const getSeverityColor = (severity) => {
    const colors = {
      low: 'text-green-400 bg-green-900/30',
      medium: 'text-yellow-400 bg-yellow-900/30',
      high: 'text-orange-400 bg-orange-900/30',
      critical: 'text-red-400 bg-red-900/30',
    };
    return colors[severity] || 'text-gray-400';
  };

  const getProtocolColor = (protocol) => {
    const colors = {
      TCP: 'text-green-400',
      UDP: 'text-blue-400',
      ICMP: 'text-red-400',
      HTTP: 'text-yellow-400',
      HTTPS: 'text-cyan-400',
      SSH: 'text-purple-400',
    };
    return colors[protocol] || 'text-white';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-cyan-400 text-xl">Загрузка...</div>
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
              <a href="/attacks" className="text-white hover:text-cyan-400 transition-colors">Атаки</a>
              <Link to="/statistics" className="text-gray-400 hover:text-cyan-400 transition-colors">Статистика</Link>
            </nav>
          </div>
          <button onClick={handleLogout} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors">
            Выход
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-20 pb-8 container mx-auto px-4">
        <h2 className="text-2xl font-bold text-white mb-6">Список атак</h2>

        {/* Filters */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6 border border-gray-700">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <select
              value={filters.protocol}
              onChange={(e) => setFilters({ ...filters, protocol: e.target.value })}
              className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
            >
              <option value="">Все протоколы</option>
              <option value="TCP">TCP</option>
              <option value="UDP">UDP</option>
              <option value="ICMP">ICMP</option>
              <option value="HTTP">HTTP</option>
              <option value="HTTPS">HTTPS</option>
              <option value="SSH">SSH</option>
            </select>

            <select
              value={filters.severity}
              onChange={(e) => setFilters({ ...filters, severity: e.target.value })}
              className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
            >
              <option value="">Все уровни</option>
              <option value="low">Низкий</option>
              <option value="medium">Средний</option>
              <option value="high">Высокий</option>
              <option value="critical">Критический</option>
            </select>

            <input
              type="text"
              placeholder="Страна..."
              value={filters.country}
              onChange={(e) => setFilters({ ...filters, country: e.target.value })}
              className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-cyan-400"
            />
          </div>
        </div>

        {/* Table */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase">Время</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase">Источник</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase">Цель</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase">Протокол</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase">Тип</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase">Страна</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase">Уровень</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {attacks.map((attack) => (
                <tr key={attack.id} className="hover:bg-gray-700/50 transition-colors">
                  <td className="px-4 py-3 text-sm text-gray-300">
                    {new Date(attack.timestamp).toLocaleString('ru-RU')}
                  </td>
                  <td className="px-4 py-3 text-sm text-white font-mono">{attack.source_ip}</td>
                  <td className="px-4 py-3 text-sm text-white font-mono">
                    {attack.target_ip}:{attack.target_port}
                  </td>
                  <td className={`px-4 py-3 text-sm font-medium ${getProtocolColor(attack.protocol)}`}>
                    {attack.protocol}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-300">{attack.attack_type}</td>
                  <td className="px-4 py-3 text-sm text-gray-300">{attack.country || 'N/A'}</td>
                  <td className={`px-4 py-3 text-sm font-medium ${getSeverityColor(attack.severity)}`}>
                    {attack.severity_display || attack.severity}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {attacks.length === 0 && (
            <div className="p-8 text-center text-gray-400">
              Атаки не найдены
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default AttacksPage;
