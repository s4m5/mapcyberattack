/**
 * Страница дашборда с 3D картой киберугроз
 * Отображает глобус с атаками в реальном времени
 */

import React, { useState, useEffect, useRef } from 'react';  // Импорт React и хуков
import Globe from 'globe.gl';  // Импорт библиотеки для 3D глобуса
import { useAuth } from '../hooks/useAuth';  // Хук аутентификации
import axios from 'axios';  // HTTP клиент

// Базовый URL API
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Цвета протоколов для визуализации
const PROTOCOL_COLORS = {
  'TCP': '#00ff00',      // Зеленый - TCP соединения
  'UDP': '#0000ff',      // Синий - UDP пакеты
  'ICMP': '#ff0000',     // Красный - ICMP ping/сканирование
  'HTTP': '#ffff00',     // Желтый - HTTP трафик
  'HTTPS': '#00ffff',    // Голубой - HTTPS защищенный
  'SSH': '#ff00ff',      // Пурпурный - SSH подключения
  'FTP': '#ffa500',      // Оранжевый - FTP передачи
  'DNS': '#800080',      // Фиолетовый - DNS запросы
};

/**
 * Компонент страницы дашборда
 * @returns {JSX.Element} Дашборд с 3D картой
 */
function DashboardPage() {
  // Получаем данные пользователя и функцию выхода
  const { user, logout } = useAuth();
  
  // Ref для контейнера глобуса
  const globeRef = useRef(null);
  
  // Ref для экземпляра Globe
  const globeInstance = useRef(null);
  
  // Состояния данных
  const [attacks, setAttacks] = useState([]);  // Список атак для отображения
  const [stats, setStats] = useState(null);    // Статистика дашборда
  const [loading, setLoading] = useState(true);// Флаг загрузки
  const [selectedAttack, setSelectedAttack] = useState(null); // Выбранная атака

  /**
   * Инициализация глобуса при монтировании компонента
   */
  useEffect(() => {
    if (globeRef.current && !globeInstance.current) {
      // Создаем новый экземпляр Globe
      globeInstance.current = Globe()
        .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
        .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
        .showAtmosphere(true)
        .atmosphereColor('#00aaff')
        .atmosphereAltitude(0.15)
        .arcColor(arc => getArcColor(arc))
        .arcDashLength(0.4)
        .arcDashGap(2)
        .arcDashAnimateTime(1500)
        .arcStroke(0.5)
        .arcCurve(0.4)
        .ringColor(() => t => `rgba(255,100,50,${1-t})`)
        .ringMaxRadius(5)
        .ringPropagationSpeed(2)
        .ringRepeatPeriod(1000)
        .htmlElementsData(attacks)
        .htmlElement(d => createHtmlElement(d))
        (globeRef.current);

      // Настройка вращения
      globeInstance.current.controls().autoRotate = true;
      globeInstance.current.controls().autoRotateSpeed = 0.8;
    }

    return () => {
      // Очистка при размонтировании
      if (globeRef.current) {
        globeRef.current.innerHTML = '';
      }
    };
  }, []);

  /**
   * Обновление данных атак на глобусе
   */
  useEffect(() => {
    if (globeInstance.current && attacks.length > 0) {
      globeInstance.current.arcsData(attacks);
      
      // Добавляем кольца в точках назначения
      const rings = attacks.map(attack => ({
        lat: attack.targetLat,
        lng: attack.targetLng,
        color: getArcColor(attack),
        maxRadius: 3,
      }));
      globeInstance.current.ringsData(rings);
    }
  }, [attacks]);

  /**
   * Загрузка данных с API
   */
  useEffect(() => {
    loadData();
    
    // Обновление данных каждые 5 секунд
    const interval = setInterval(loadData, 5000);
    
    return () => clearInterval(interval);
  }, []);

  /**
   * Загрузка данных об атаках и статистике
   */
  async function loadData() {
    try {
      // Установка токена авторизации
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      // Параллельная загрузка атак и статистики
      const [attacksResponse, statsResponse] = await Promise.all([
        axios.get(`${API_URL}/live/?limit=100`),
        axios.get(`${API_URL}/dashboard/?hours=24`),
      ]);

      // Обработка данных атак
      const attacksData = attacksResponse.data.results || [];
      const formattedAttacks = attacksData
        .filter(a => a.latitude && a.longitude)
        .map(attack => ({
          startLat: parseFloat(attack.latitude),
          startLng: parseFloat(attack.longitude),
          endLat: 55.7558,  // Москва (целевой сервер)
          endLng: 37.6173,
          color: getProtocolColor(attack.protocol),
          protocol: attack.protocol,
          sourceIp: attack.source_ip,
          targetPort: attack.target_port,
          attackType: attack.attack_type,
          timestamp: attack.timestamp,
          country: attack.country,
        }));

      setAttacks(formattedAttacks);
      setStats(statsResponse.data);
      setLoading(false);
    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      setLoading(false);
    }
  }

  /**
   * Получение цвета дуги по протоколу
   * @param {Object} arc - Данные дуги
   * @returns {string} HEX цвет
   */
  function getArcColor(arc) {
    return getProtocolColor(arc.protocol);
  }

  /**
   * Получение цвета по названию протокола
   * @param {string} protocol - Название протокола
   * @returns {string} HEX цвет
   */
  function getProtocolColor(protocol) {
    return PROTOCOL_COLORS[protocol?.toUpperCase()] || '#ffffff';
  }

  /**
   * Создание HTML элемента для метки на глобусе
   * @param {Object} d - Данные атаки
   * @returns {HTMLElement} DOM элемент
   */
  function createHtmlElement(d) {
    const el = document.createElement('div');
    el.style.width = '8px';
    el.style.height = '8px';
    el.style.borderRadius = '50%';
    el.style.background = getProtocolColor(d.protocol);
    el.style.boxShadow = `0 0 10px ${getProtocolColor(d.protocol)}`;
    el.style.cursor = 'pointer';
    el.onclick = () => setSelectedAttack(d);
    return el;
  }

  /**
   * Обработчик выхода
   */
  function handleLogout() {
    logout();
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-cyan-400 text-xl">Загрузка карты...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Верхняя панель */}
      <header className="fixed top-0 left-0 right-0 z-10 bg-gray-900/90 backdrop-blur border-b border-gray-700">
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold text-cyan-400">🛡️ Карта Киберугроз</h1>
            <nav className="hidden md:flex space-x-4">
              <a href="/" className="text-white hover:text-cyan-400 transition-colors">Дашборд</a>
              <a href="/attacks" className="text-gray-400 hover:text-cyan-400 transition-colors">Атаки</a>
              <a href="/statistics" className="text-gray-400 hover:text-cyan-400 transition-colors">Статистика</a>
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-gray-400 text-sm">
              👤 {user?.username}
            </span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
            >
              Выход
            </button>
          </div>
        </div>
      </header>

      {/* Контейнер глобуса */}
      <div ref={globeRef} className="w-full h-screen" />

      {/* Панель статистики */}
      {stats && (
        <div className="fixed bottom-4 left-4 z-10 bg-gray-800/90 backdrop-blur rounded-lg p-4 border border-gray-700 max-w-xs">
          <h3 className="text-lg font-semibold text-white mb-3">📊 Статистика за 24ч</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Всего атак:</span>
              <span className="text-cyan-400 font-bold">{stats.total_attacks}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Уникальных IP:</span>
              <span className="text-green-400 font-bold">{stats.unique_sources}</span>
            </div>
          </div>
          
          {stats.top_countries?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-700">
              <h4 className="text-sm font-medium text-gray-300 mb-2">Топ стран:</h4>
              <ul className="space-y-1">
                {stats.top_countries.slice(0, 5).map((item, idx) => (
                  <li key={idx} className="flex justify-between text-sm">
                    <span className="text-gray-400">{item.country}</span>
                    <span className="text-white">{item.count}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Легенда протоколов */}
      <div className="fixed bottom-4 right-4 z-10 bg-gray-800/90 backdrop-blur rounded-lg p-4 border border-gray-700">
        <h3 className="text-sm font-semibold text-white mb-2">Протоколы:</h3>
        <div className="grid grid-cols-2 gap-2 text-xs">
          {Object.entries(PROTOCOL_COLORS).slice(0, 6).map(([protocol, color]) => (
            <div key={protocol} className="flex items-center space-x-2">
              <div 
                className="w-3 h-3 rounded" 
                style={{ backgroundColor: color, boxShadow: `0 0 5px ${color}` }}
              />
              <span className="text-gray-300">{protocol}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Модальное окно выбранной атаки */}
      {selectedAttack && (
        <div 
          className="fixed inset-0 z-20 flex items-center justify-center bg-black/50"
          onClick={() => setSelectedAttack(null)}
        >
          <div 
            className="bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 border border-gray-700"
            onClick={e => e.stopPropagation()}
          >
            <h3 className="text-xl font-bold text-white mb-4">Информация об атаке</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Источник:</span>
                <span className="text-white font-mono">{selectedAttack.sourceIp}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Страна:</span>
                <span className="text-white">{selectedAttack.country}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Протокол:</span>
                <span className="text-white">{selectedAttack.protocol}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Порт:</span>
                <span className="text-white">{selectedAttack.targetPort}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Тип:</span>
                <span className="text-white">{selectedAttack.attackType}</span>
              </div>
            </div>
            <button
              onClick={() => setSelectedAttack(null)}
              className="mt-4 w-full py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded transition-colors"
            >
              Закрыть
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;
