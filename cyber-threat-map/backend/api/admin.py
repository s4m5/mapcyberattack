"""
Административная панель Django для управления моделями карты киберугроз.
Предоставляет интерфейс для просмотра и управления данными через веб-интерфейс.
"""

from django.contrib import admin  # Импортируем модуль административной панели
from .models import CyberAttack, AttackStatistics, SystemConfig, User  # Импортируем модели


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели пользователя.
    Отображает список пользователей с основными полями.
    """
    
    list_display = [  # Поля отображаемые в списке пользователей
        'username',  # Имя пользователя
        'email',  # Email адрес
        'first_name',  # Имя
        'last_name',  # Фамилия
        'is_active',  # Статус активности
        'created_at',  # Дата создания
        'updated_at',  # Дата обновления
    ]
    
    list_filter = [  # Фильтры в правой панели
        'is_active',  # Фильтр по активности
        'created_at',  # Фильтр по дате создания
    ]
    
    search_fields = [  # Поля для поиска
        'username',  # Поиск по имени пользователя
        'email',  # Поиск по email
        'first_name',  # Поиск по имени
        'last_name',  # Поиск по фамилии
    ]
    
    ordering = ['-created_at']  # Сортировка по умолчанию (новые первыми)


@admin.register(CyberAttack)
class CyberAttackAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели кибератаки.
    Предоставляет детальный просмотр и фильтрацию атак.
    """
    
    list_display = [  # Поля отображаемые в списке атак
        'source_ip',  # IP адрес источника
        'target_ip',  # IP адрес цели
        'target_port',  # Целевой порт
        'protocol',  # Протокол
        'attack_type',  # Тип атаки
        'severity',  # Уровень опасности
        'country',  # Страна источника
        'timestamp',  # Время атаки
    ]
    
    list_filter = [  # Фильтры в правой панели
        'protocol',  # Фильтр по протоколу
        'attack_type',  # Фильтр по типу атаки
        'severity',  # Фильтр по уровню опасности
        'country',  # Фильтр по стране
        'firewall_action',  # Фильтр по действию фаервола
        'timestamp',  # Фильтр по времени
    ]
    
    search_fields = [  # Поля для поиска
        'source_ip',  # Поиск по IP источника
        'target_ip',  # Поиск по IP цели
        'attack_type',  # Поиск по типу атаки
        'country',  # Поиск по стране
        'city',  # Поиск по городу
    ]
    
    readonly_fields = [  # Поля только для чтения
        'created_at',  # Дата создания
        'updated_at',  # Дата обновления
    ]
    
    ordering = ['-timestamp']  # Сортировка по умолчанию (новые первыми)
    
    date_hierarchy = 'timestamp'  # Иерархическая навигация по дате
    
    fieldsets = (  # Группировка полей в форме редактирования
        ('Основная информация', {
            'fields': (
                'source_ip',  # IP источника
                'target_ip',  # IP цели
                'source_port',  # Порт источника
                'target_port',  # Порт цели
            )
        }),
        ('Классификация атаки', {
            'fields': (
                'protocol',  # Протокол
                'attack_type',  # Тип атаки
                'vulnerability_type',  # Тип уязвимости
                'severity',  # Уровень опасности
            )
        }),
        ('Геолокация', {
            'fields': (
                'country',  # Страна
                'city',  # Город
                'latitude',  # Широта
                'longitude',  # Долгота
            )
        }),
        ('Метаданные', {
            'fields': (
                'timestamp',  # Время атаки
                'firewall_action',  # Действие фаервола
                'raw_log',  # Исходный лог
            )
        }),
        ('Системные поля', {
            'fields': (
                'created_at',  # Дата создания
                'updated_at',  # Дата обновления
            ),
            'classes': ('collapse',),  # Свернутая секция
        }),
    )


@admin.register(AttackStatistics)
class AttackStatisticsAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели статистики атак.
    Отображает агрегированные данные за каждый день.
    """
    
    list_display = [  # Поля отображаемые в списке статистики
        'date',  # Дата статистики
        'total_attacks',  # Общее количество атак
        'unique_sources',  # Количество уникальных источников
        'created_at',  # Дата создания записи
        'updated_at',  # Дата обновления записи
    ]
    
    list_filter = [  # Фильтры в правой панели
        'date',  # Фильтр по дате
    ]
    
    search_fields = [  # Поля для поиска
        'date',  # Поиск по дате
    ]
    
    readonly_fields = [  # Поля только для чтения
        'top_attack_types',  # Топ типов атак (JSON)
        'top_vulnerabilities',  # Топ уязвимостей (JSON)
        'top_ports',  # Топ портов (JSON)
        'top_countries',  # Топ стран (JSON)
        'created_at',  # Дата создания
        'updated_at',  # Дата обновления
    ]
    
    ordering = ['-date']  # Сортировка по умолчанию (новые первыми)
    
    date_hierarchy = 'date'  # Иерархическая навигация по дате


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели системной конфигурации.
    Позволяет управлять настройками системы через админ-панель.
    """
    
    list_display = [  # Поля отображаемые в списке настроек
        'key',  # Ключ настройки
        'value',  # Значение настройки
        'description',  # Описание настройки
        'updated_at',  # Дата последнего обновления
    ]
    
    list_filter = [  # Фильтры в правой панели
        'updated_at',  # Фильтр по дате обновления
    ]
    
    search_fields = [  # Поля для поиска
        'key',  # Поиск по ключу
        'description',  # Поиск по описанию
    ]
    
    readonly_fields = [  # Поля только для чтения
        'updated_at',  # Дата обновления
    ]
    
    ordering = ['key']  # Сортировка по ключу
