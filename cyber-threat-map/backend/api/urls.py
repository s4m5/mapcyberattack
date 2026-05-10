"""
URL конфигурация для API карты киберугроз.
Определяет маршруты (endpoints) для всех представлений API.
"""

from django.urls import path, include  # Импортируем функции для работы с URL
from rest_framework.routers import DefaultRouter  # Импортируем роутер для автоматической генерации URL
from . import views  # Импортируем представления из текущего приложения

# Создаем роутер для автоматической регистрации ViewSet
router = DefaultRouter()

# Регистрируем ViewSet в роутере
# router.register создаст следующие URL:
# /api/attacks/ - список и создание атак
# /api/attacks/{id}/ - детали, обновление, удаление конкретной атаки
router.register(r'attacks', views.CyberAttackViewSet, basename='attack')

# Регистрируем статистику атак (только чтение)
# /api/statistics/ - список статистики
# /api/statistics/{id}/ - детали конкретной записи статистики
router.register(r'statistics', views.AttackStatisticsViewSet, basename='statistics')

# Регистрируем системную конфигурацию
# /api/config/ - список настроек
# /api/config/{id}/ - детали конкретной настройки
router.register(r'config', views.SystemConfigViewSet, basename='config')

# Определяем urlpatterns - список всех URL паттернов приложения
urlpatterns = [
    # Включаем URL созданные роутером для ViewSet
    path('', include(router.urls)),
    
    # URL для аутентификации пользователя
    path('auth/login/', views.login_view, name='login'),  # Вход пользователя
    path('auth/logout/', views.logout_view, name='logout'),  # Выход пользователя
    path('auth/register/', views.register_view, name='register'),  # Регистрация нового пользователя
    
    # URL для получения статистики дашборда
    path('dashboard/stats/', views.dashboard_stats_view, name='dashboard-stats'),  # Общая статистика
    
    # URL для получения данных в реальном времени
    path('attacks/live/', views.live_attacks_view, name='live-attacks'),  # Последние атаки
    
    # URL для получения геоданных об атаках
    path('attacks/geo/', views.geo_attacks_view, name='geo-attacks'),  # Геоданные атак
]
