"""
Модели данных для приложения карты киберугроз.
Определяет структуру базы данных для хранения информации об атаках, пользователях и статистике.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Кастомная модель пользователя с расширенными полями.
    Наследуется от стандартной модели Django AbstractUser.
    """
    email = models.EmailField('email address', unique=True)  # Уникальный email пользователя
    is_active = models.BooleanField(default=True)  # Активен ли пользователь
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания пользователя
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления

    class Meta:
        """Мета-настройки модели User."""
        verbose_name = 'Пользователь'  # Человекочитаемое название модели
        verbose_name_plural = 'Пользователи'  # Множественное число
        ordering = ['-created_at']  # Сортировка по дате создания (новые первыми)

    def __str__(self):
        """Строковое представление пользователя (возвращает username)."""
        return self.username


class CyberAttack(models.Model):
    """
    Модель для хранения информации о кибератаке.
    Содержит все данные об одной атаке: IP адреса, порты, протоколы, геолокацию.
    """
    # Поля для исходных данных атаки
    source_ip = models.GenericIPAddressField('IP адрес источника', protocol='IPv4')  # IP атакующего
    target_ip = models.GenericIPAddressField('IP адрес цели', protocol='IPv4')  # IP цели (наш сервер)
    source_port = models.PositiveIntegerField('Порт источника', null=True, blank=True)  # Порт атакующего
    target_port = models.PositiveIntegerField('Порт цели', null=True, blank=True)  # Атакуемый порт
    
    # Поля для классификации атаки
    protocol = models.CharField('Протокол', max_length=20, default='TCP')  # Протокол (TCP/UDP/ICMP)
    attack_type = models.CharField('Тип атаки', max_length=100, default='Unknown')  # Тип вектора атаки
    vulnerability_type = models.CharField('Тип уязвимости', max_length=100, blank=True, default='')  # Тип уязвимости
    
    # Геолокация источника атаки
    country = models.CharField('Страна', max_length=100, blank=True, default='')  # Страна атакующего
    city = models.CharField('Город', max_length=100, blank=True, default='')  # Город атакующего
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)  # Координаты
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)  # Координаты
    
    # Метаданные атаки
    timestamp = models.DateTimeField('Время атаки', default=timezone.now)  # Время обнаружения
    severity = models.CharField('Уровень опасности', max_length=20, choices=[
        ('low', 'Низкий'),  # Низкая опасность
        ('medium', 'Средний'),  # Средняя опасность
        ('high', 'Высокий'),  # Высокая опасность
        ('critical', 'Критический'),  # Критическая опасность
    ], default='medium')  # Уровень опасности по умолчанию
    
    # Дополнительные данные
    raw_log = models.TextField('Исходный лог', blank=True, default='')  # Оригинальная строка лога
    firewall_action = models.CharField('Действие фаервола', max_length=20, choices=[
        ('DROP', 'Заблокировано'),  # Пакет отброшен
        ('REJECT', 'Отклонено'),  # Пакет отклонен с уведомлением
        ('ACCEPT', 'Разрешено'),  # Пакет пропущен
        ('LOG', 'Записано в лог'),  # Только логирование
    ], blank=True, default='')  # Действие фаервола
    
    # Системные поля
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)  # Дата добавления в БД
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)  # Дата последнего изменения
    
    class Meta:
        """Мета-настройки модели CyberAttack."""
        verbose_name = 'Кибератака'  # Человекочитаемое название
        verbose_name_plural = 'Кибератаки'  # Множественное число
        ordering = ['-timestamp']  # Сортировка по времени (новые первыми)
        indexes = [
            models.Index(fields=['-timestamp']),  # Индекс для быстрой сортировки по времени
            models.Index(fields=['source_ip']),  # Индекс для поиска по IP источника
            models.Index(fields=['target_ip']),  # Индекс для поиска по IP цели
            models.Index(fields=['protocol']),  # Индекс для фильтрации по протоколу
            models.Index(fields=['attack_type']),  # Индекс для фильтрации по типу атаки
            models.Index(fields=['country']),  # Индекс для фильтрации по стране
        ]

    def __str__(self):
        """Строковое представление атаки (источник -> цель)."""
        return f"{self.source_ip} -> {self.target_ip}:{self.target_port}"


class AttackStatistics(models.Model):
    """
    Модель для хранения агрегированной статистики атак.
    Обновляется периодически для быстрого доступа к топ-N данным.
    """
    # Период статистики
    date = models.DateField('Дата', unique=True)  # Дата для которой собрана статистика
    
    # Топ-10 типов атак (хранятся как JSON)
    top_attack_types = models.JSONField('Топ типов атак', default=list)  # [{'type': 'SSH', 'count': 100}, ...]
    top_vulnerabilities = models.JSONField('Топ уязвимостей', default=list)  # [{'type': 'CVE-XXX', 'count': 50}, ...]
    top_ports = models.JSONField('Топ портов', default=list)  # [{'port': 22, 'count': 200}, ...]
    top_countries = models.JSONField('Топ стран', default=list)  # [{'country': 'Russia', 'count': 150}, ...]
    
    # Общая статистика
    total_attacks = models.PositiveIntegerField('Всего атак', default=0)  # Общее количество атак
    unique_sources = models.PositiveIntegerField('Уникальных источников', default=0)  # Количество уникальных IP
    
    # Системные поля
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)  # Дата добавления
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)  # Дата обновления
    
    class Meta:
        """Мета-настройки модели AttackStatistics."""
        verbose_name = 'Статистика атак'
        verbose_name_plural = 'Статистика атак'
        ordering = ['-date']  # Сортировка по дате (новые первыми)

    def __str__(self):
        """Строковое представление статистики (дата и количество атак)."""
        return f"Статистика за {self.date} ({self.total_attacks} атак)"


class SystemConfig(models.Model):
    """
    Модель для хранения конфигурации системы.
    Позволяет настраивать параметры без изменения кода.
    """
    key = models.CharField('Ключ', max_length=100, unique=True)  # Уникальный ключ настройки
    value = models.TextField('Значение')  # Значение настройки
    description = models.CharField('Описание', max_length=500, blank=True, default='')  # Описание настройки
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)  # Дата последнего изменения
    
    class Meta:
        """Мета-настройки модели SystemConfig."""
        verbose_name = 'Настройка системы'
        verbose_name_plural = 'Настройки системы'

    def __str__(self):
        """Строковое представление настройки (ключ = значение)."""
        return f"{self.key} = {self.value}"
