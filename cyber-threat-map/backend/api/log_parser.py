"""
Модуль для парсинга системных логов и извлечения информации об атаках.
Поддерживает различные форматы логов: syslog, iptables, nftables, ufw.
"""

import re
import socket
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

# Настройка логгера для модуля парсера
logger = logging.getLogger(__name__)


class LogParser:
    """
    Класс для парсинга различных форматов системных логов.
    Извлекает информацию об IP адресах, портах, протоколах из логов фаервола.
    """
    
    # Регулярные выражения для извлечения данных из логов
    
    # Шаблон для IPv4 адреса (четыре октета разделенных точками)
    IPV4_PATTERN = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    
    # Шаблон для порта (число от 1 до 65535)
    PORT_PATTERN = r'\b(?:DPT|SPT|PORT|port)[:=](\d+)\b'
    
    # Шаблон для протокола (TCP, UDP, ICMP)
    PROTOCOL_PATTERN = r'\b(?:PROTO|protocol)[:=]?(TCP|UDP|ICMP)\b'
    
    # Шаблон для действия фаервола (DROP, REJECT, ACCEPT, LOG)
    ACTION_PATTERN = r'\b(DROP|REJECT|ACCEPT|LOG|BLOCK)\b'
    
    # Шаблон для даты в различных форматах
    DATE_PATTERNS = [
        r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',  # Syslog формат: Jan  5 10:15:30
        r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',  # ISO формат: 2024-01-05 10:15:30
        r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})',  # Apache формат: 05/Jan/2024:10:15:30
    ]
    
    # Словарь известных портов и соответствующих им протоколов/сервисов
    KNOWN_PORTS = {
        22: ('SSH', 'SSH'),
        23: ('TELNET', 'Telnet'),
        25: ('SMTP', 'SMTP'),
        53: ('DNS', 'DNS'),
        80: ('HTTP', 'HTTP'),
        443: ('HTTPS', 'HTTPS'),
        21: ('FTP', 'FTP'),
        20: ('FTP', 'FTP-Data'),
        110: ('POP3', 'POP3'),
        143: ('IMAP', 'IMAP'),
        3306: ('MySQL', 'MySQL'),
        5432: ('PostgreSQL', 'PostgreSQL'),
        6379: ('Redis', 'Redis'),
        27017: ('MongoDB', 'MongoDB'),
        8080: ('HTTP-ALT', 'HTTP Alternate'),
        3389: ('RDP', 'Remote Desktop'),
        445: ('SMB', 'SMB'),
        139: ('NetBIOS', 'NetBIOS'),
        135: ('RPC', 'RPC'),
        1433: ('MSSQL', 'Microsoft SQL'),
        1521: ('Oracle', 'Oracle DB'),
        5900: ('VNC', 'VNC'),
        6000: ('X11', 'X Window'),
        8443: ('HTTPS-ALT', 'HTTPS Alternate'),
        9000: ('PHP-FPM', 'PHP FastCGI'),
    }
    
    # Типы атак по сигнатурам в логах
    ATTACK_SIGNATURES = {
        r'PORTSCAN': 'Port Scan',  # Сканирование портов
        r'SYN': 'SYN Flood',  # SYN флуд атака
        r'FIN': 'FIN Scan',  # FIN сканирование
        r'XMAS': 'XMAS Scan',  # XMAS сканирование
        r'NULL': 'NULL Scan',  # NULL сканирование
        r'ACK': 'ACK Scan',  # ACK сканирование
        r'WINDOW': 'Window Scan',  # Window сканирование
        r'FRAGMENT': 'Fragment Attack',  # Фрагментация пакетов
        r'BROADCAST': 'Broadcast Attack',  # Broadcast атака
        r'MULTICAST': 'Multicast Attack',  # Multicast атака
        r'LAND': 'LAND Attack',  # LAND атака
        r'SPOOF': 'Spoofing Attack',  # Спуфинг атака
        r'DDOS': 'DDoS Attack',  # DDoS атака
        r'DOS': 'DoS Attack',  # DoS атака
        r'BRUTE': 'Brute Force',  # Перебор паролей
        r'INVALID': 'Invalid Packet',  # Неверный пакет
        r'MALFORMED': 'Malformed Packet',  # Поврежденный пакет
    }

    def __init__(self):
        """Инициализация парсера с компиляцией регулярных выражений."""
        # Компиляция основных регулярных выражений для производительности
        self.ipv4_regex = re.compile(self.IPV4_PATTERN)
        self.port_regex = re.compile(self.PORT_PATTERN, re.IGNORECASE)
        self.protocol_regex = re.compile(self.PROTOCOL_PATTERN, re.IGNORECASE)
        self.action_regex = re.compile(self.ACTION_PATTERN, re.IGNORECASE)
        
        # Компиляция паттернов для дат
        self.date_regexes = [re.compile(pattern) for pattern in self.DATE_PATTERNS]
        
        # Компиляция паттернов для типов атак
        self.attack_patterns = {
            re.compile(pattern, re.IGNORECASE): attack_type 
            for pattern, attack_type in self.ATTACK_SIGNATURES.items()
        }

    def parse_line(self, log_line: str) -> Optional[Dict[str, Any]]:
        """
        Парсит одну строку лога и извлекает информацию об атаке.
        
        Args:
            log_line: Строка лога для парсинга
            
        Returns:
            Словарь с данными об атаке или None если строка не содержит полезной информации
        """
        # Пропускаем пустые строки
        if not log_line or not log_line.strip():
            return None
        
        # Извлекаем все IP адреса из строки
        ip_addresses = self.ipv4_regex.findall(log_line)
        
        # Если нет IP адресов, пропускаем строку
        if len(ip_addresses) < 1:
            return None
        
        # Определяем источник и цель
        # В логах фаервола обычно первый IP - источник, второй - цель
        source_ip = ip_addresses[0] if ip_addresses else None
        target_ip = ip_addresses[1] if len(ip_addresses) > 1 else self.get_local_ip()
        
        # Извлекаем порты
        ports = self.port_regex.findall(log_line)
        source_port = int(ports[0]) if len(ports) > 0 else None
        target_port = int(ports[1]) if len(ports) > 1 else (int(ports[0]) if ports else None)
        
        # Извлекаем протокол
        protocol_match = self.protocol_regex.search(log_line)
        protocol = protocol_match.group(1).upper() if protocol_match else self.detect_protocol_by_port(target_port)
        
        # Извлекаем действие фаервола
        action_match = self.action_regex.search(log_line)
        firewall_action = action_match.group(1).upper() if action_match else 'LOG'
        
        # Определяем тип атаки по сигнатурам
        attack_type = self.detect_attack_type(log_line)
        
        # Если тип атаки не определен, определяем по порту
        if attack_type == 'Unknown' and target_port:
            attack_type = f"Attack on {self.KNOWN_PORTS.get(target_port, ('Unknown', 'Unknown'))[0]}"
        
        # Определяем уровень опасности
        severity = self.calculate_severity(attack_type, firewall_action, target_port)
        
        # Извлекаем дату из лога
        timestamp = self.extract_timestamp(log_line)
        
        # Формируем результат
        result = {
            'source_ip': source_ip,
            'target_ip': target_ip,
            'source_port': source_port,
            'target_port': target_port,
            'protocol': protocol,
            'attack_type': attack_type,
            'vulnerability_type': '',  # Будет заполнено позже
            'firewall_action': firewall_action,
            'severity': severity,
            'timestamp': timestamp,
            'raw_log': log_line.strip(),
        }
        
        return result

    def detect_protocol_by_port(self, port: Optional[int]) -> str:
        """
        Определяет протокол по номеру порта.
        
        Args:
            port: Номер порта
            
        Returns:
            Название протокола (TCP, UDP, HTTP, HTTPS, SSH, etc.)
        """
        if port is None:
            return 'TCP'  # Протокол по умолчанию
        
        if port in self.KNOWN_PORTS:
            return self.KNOWN_PORTS[port][0]
        
        # Стандартные диапазоны портов
        if port == 53:
            return 'DNS'
        elif port in [80, 8080, 8000]:
            return 'HTTP'
        elif port in [443, 8443]:
            return 'HTTPS'
        elif port == 22:
            return 'SSH'
        elif port in [20, 21]:
            return 'FTP'
        elif port < 1024:
            return 'TCP'  # Привилегированные порты обычно TCP
        else:
            return 'TCP'  # Протокол по умолчанию

    def detect_attack_type(self, log_line: str) -> str:
        """
        Определяет тип атаки по сигнатурам в строке лога.
        
        Args:
            log_line: Строка лога для анализа
            
        Returns:
            Название типа атаки или 'Unknown' если не определено
        """
        for pattern, attack_type in self.attack_patterns.items():
            if pattern.search(log_line):
                return attack_type
        
        return 'Unknown'

    def calculate_severity(self, attack_type: str, firewall_action: str, target_port: Optional[int]) -> str:
        """
        Вычисляет уровень опасности атаки на основе типа атаки и других факторов.
        
        Args:
            attack_type: Тип атаки
            firewall_action: Действие фаервола (DROP, ACCEPT, etc.)
            target_port: Целевой порт
            
        Returns:
            Уровень опасности: low, medium, high, critical
        """
        # Критические атаки
        critical_attacks = ['DDoS Attack', 'DoS Attack', 'LAND Attack']
        if any(attack in attack_type for attack in critical_attacks):
            return 'critical'
        
        # Высокая опасность
        high_attacks = ['Brute Force', 'Spoofing Attack', 'Port Scan']
        if any(attack in attack_type for attack in high_attacks):
            return 'high'
        
        # Средняя опасность для заблокированных атак на важные порты
        important_ports = [22, 23, 3389, 3306, 5432, 27017, 6379]
        if firewall_action in ['DROP', 'REJECT'] and target_port in important_ports:
            return 'medium'
        
        # Низкая опасность для остальных случаев
        return 'low'

    def extract_timestamp(self, log_line: str) -> datetime:
        """
        Извлекает дату и время из строки лога.
        
        Args:
            log_line: Строка лога
            
        Returns:
            Объект datetime или текущее время если дата не найдена
        """
        # Текущий год для подстановки (syslog не содержит год)
        current_year = datetime.now().year
        
        for regex in self.date_regexes:
            match = regex.search(log_line)
            if match:
                date_str = match.group(1)
                try:
                    # Пробуем различные форматы даты
                    for fmt in ['%b %d %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d/%b/%Y:%H:%M:%S']:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            # Если год не указан, используем текущий
                            if dt.year == 1900:
                                dt = dt.replace(year=current_year)
                            return dt
                        except ValueError:
                            continue
                except Exception as e:
                    logger.warning(f"Ошибка при парсинге даты '{date_str}': {e}")
        
        # Возвращаем текущее время если дата не найдена
        return datetime.now()

    @staticmethod
    def get_local_ip() -> str:
        """
        Получает локальный IP адрес сервера.
        
        Returns:
            Локальный IP адрес или '127.0.0.1' если не удалось определить
        """
        try:
            # Создаем сокет для определения внешнего IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return '127.0.0.1'


class SyslogMonitor:
    """
    Класс для мониторинга syslog файла в реальном времени.
    Использует polling для отслеживания новых записей в логе.
    """
    
    def __init__(self, log_file_path: str, parser: LogParser):
        """
        Инициализация монитора логов.
        
        Args:
            log_file_path: Путь к файлу лога
            parser: Экземпляр LogParser для парсинга строк
        """
        self.log_file_path = Path(log_file_path)
        self.parser = parser
        self.position = 0  # Текущая позиция в файле
        self.inode = None  # Inode файла для отслеживания ротации

    def check_rotation(self) -> bool:
        """
        Проверяет, не была ли повернута файл логов.
        
        Returns:
            True если файл был повернут, False иначе
        """
        try:
            current_inode = self.log_file_path.stat().st_ino
            if self.inode is not None and current_inode != self.inode:
                logger.info("Обнаружена ротация логов, сброс позиции")
                self.position = 0
                self.inode = current_inode
                return True
            self.inode = current_inode
            return False
        except FileNotFoundError:
            logger.warning(f"Файл лога {self.log_file_path} не найден")
            return False

    def read_new_lines(self) -> List[Dict[str, Any]]:
        """
        Читает новые строки из файла лога с последней позиции.
        
        Returns:
            Список распарсенных записей об атаках
        """
        attacks = []
        
        # Проверяем существование файла
        if not self.log_file_path.exists():
            logger.warning(f"Файл лога {self.log_file_path} не существует")
            return attacks
        
        # Проверяем ротацию
        self.check_rotation()
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Переходим к последней известной позиции
                f.seek(self.position)
                
                # Читаем новые строки
                for line in f:
                    # Парсим строку
                    parsed = self.parser.parse_line(line)
                    if parsed:
                        attacks.append(parsed)
                
                # Сохраняем новую позицию
                self.position = f.tell()
                
        except PermissionError:
            logger.error(f"Нет прав на чтение файла {self.log_file_path}")
        except Exception as e:
            logger.error(f"Ошибка при чтении лога: {e}")
        
        return attacks


def get_protocol_color(protocol: str) -> str:
    """
    Возвращает цвет для визуализации в зависимости от протокола.
    
    Args:
        protocol: Название протокола
        
    Returns:
        HEX код цвета
    """
    colors = {
        'TCP': '#00ff00',  # Зеленый
        'UDP': '#0000ff',  # Синий
        'ICMP': '#ff0000',  # Красный
        'HTTP': '#ffff00',  # Желтый
        'HTTPS': '#00ffff',  # Голубой
        'SSH': '#ff00ff',  # Маджента
        'FTP': '#ffa500',  # Оранжевый
        'DNS': '#800080',  # Фиолетовый
        'SMTP': '#00ff7f',  # Весенне-зеленый
        'MYSQL': '#ff6347',  # Томатный
        'POSTGRESQL': '#4169e1',  # Королевский синий
        'REDIS': '#dc143c',  # Малиновый
        'MONGODB': '#32cd32',  # Лаймовый
        'RDP': '#ffd700',  # Золотой
        'SMB': '#ff4500',  # Оранжево-красный
    }
    
    return colors.get(protocol.upper(), '#ffffff')  # Белый по умолчанию
