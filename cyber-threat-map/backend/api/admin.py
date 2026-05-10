"""
Административная панель Django для приложения карты киберугроз.
Предоставляет интерфейс для управления данными через /admin/
"""

from django.contrib import admin  # Импорт административной панели Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # Базовый класс админки пользователя
from api.models import User, CyberAttack, AttackStatistics, SystemConfig  # Импорт моделей


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Административная панель для модели пользователя.
    Наследуется от стандартной UserAdmin с кастомизацией.
    """
    # Поля отображаемые в списке пользователей
    list_display = [
        'username',  # Имя пользователя
        'email',  # Email
        'is_active',  # Статус активности
        'created_at',  # Дата создания
        'updated_at',  # Дата обновления
    ]
    
    # Поля для фильтрации в правой панели
    list_filter = ['is_active', 'created_at', 'updated_at']
    
    # Поля для поиска по пользователям
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Поля которые можно редактировать прямо из списка
    list_editable = ['is_active']
    
    # Порядок сортировки по умолчанию
    ordering = ['-created_at']
    
    # Группировка полей в форме редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Основная информация
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    # Поля при создании нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(CyberAttack)
class CyberAttackAdmin(admin.ModelAdmin):
    """
    Административная панель для модели кибератаки.
    Позволяет просматривать и фильтровать атаки.
    """
    # Поля отображаемые в списке атак
    list_display = [
        'source_ip',  # IP источника
        'target_ip',  # IP цели
        'target_port',  # Порт цели
        'protocol',  # Протокол
        'attack_type',  # Тип атаки
        'country',  # Страна
        'severity',  # Уровень опасности
        'timestamp',  # Время атаки
    ]
    
    # Поля для фильтрации
    list_filter = [
        'protocol',  # По протоколу
        'severity',  # По уровню опасности
        'firewall_action',  # По действию фаервола
        'country',  # По стране
        'attack_type',  # По типу атаки
        'timestamp',  # По времени
    ]
    
    # Поля для поиска
    search_fields = [
        'source_ip',  # Поиск по IP источника
        'target_ip',  # Поиск по IP цели
        'attack_type',  # Поиск по типу атаки
        'country',  # Поиск по стране
        'raw_log',  # Поиск в исходном логе
    ]
    
    # Поля только для чтения (нельзя изменять через админку)
    readonly_fields = [
        'source_ip', 'target_ip', 'source_port', 'target_port',
        'protocol', 'attack_type', 'vulnerability_type',
        'country', 'city', 'latitude', 'longitude',
        'timestamp', 'severity', 'firewall_action',
        'raw_log', 'created_at', 'updated_at',
    ]
    
    # Порядок сортировки
    ordering = ['-timestamp']
    
    # Дата иерархия для навигации по датам
    date_hierarchy = 'timestamp'
    
    # Группировка полей в форме просмотра
    fieldsets = (
        ('Сетевая информация', {
            'fields': (
                'source_ip', 'source_port',
                'target_ip', 'target_port',
                'protocol',
            )
        }),
        ('Классификация атаки', {
            'fields': (
                'attack_type',
                'vulnerability_type',
                'severity',
                'firewall_action',
            )
        }),
        ('Геолокация', {
            'fields': (
                'country',
                'city',
                'latitude',
                'longitude',
            ),
            'classes': ('collapse',),
        }),
        ('Метаданные', {
            'fields': (
                'timestamp',
                'raw_log',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    # Количество записей на странице
    list_per_page = 50


@admin.register(AttackStatistics)
class AttackStatisticsAdmin(admin.ModelAdmin):
    """
    Административная панель для модели статистики атак.
    """
    # Поля в списке
    list_display = [
        'date',  # Дата статистики
        'total_attacks',  # Всего атак
        'unique_sources',  # Уникальных источников
        'created_at',  # Дата создания
    ]
    
    # Фильтры
    list_filter = ['date', 'created_at']
    
    # Поля только для чтения
    readonly_fields = [
        'date',
        'top_attack_types',
        'top_vulnerabilities',
        'top_ports',
        'top_countries',
        'total_attacks',
        'unique_sources',
        'created_at',
        'updated_at',
    ]
    
    # Сортировка
    ordering = ['-date']
    
    # Группировка полей
    fieldsets = (
        ('Основная информация', {
            'fields': ('date', 'total_attacks', 'unique_sources')
        }),
        ('Топ показателей', {
            'fields': (
                'top_attack_types',
                'top_vulnerabilities',
                'top_ports',
                'top_countries',
            ),
            'classes': ('collapse',),
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    """
    Административная панель для системных настроек.
    """
    # Поля в списке
    list_display = [
        'key',  # Ключ настройки
        'value',  # Значение (обрезается)
        'description',  # Описание
        'updated_at',  # Дата обновления
    ]
    
    # Поля для поиска
    search_fields = ['key', 'description']
    
    # Поля только для чтения
    readonly_fields = ['updated_at']
    
    # Сортировка
    ordering = ['key']


# Заголовок административной панели
admin.site.site_header = 'Карта Киберугроз - Администрирование'
admin.site.site_title = 'Карта Киберугроз Admin'
admin.site.index_title = 'Панель управления'
