"""
URL маршруты для API приложения карты киберугроз.
Определяет эндпоинты для доступа к атакам, статистике и аутентификации.
"""

from django.urls import path, include  # Импорт функций для определения URL паттернов
from rest_framework.routers import DefaultRouter  # Импорт роутера DRF для автоматической генерации URL
from api.views import (
    CyberAttackViewSet,  # ViewSet для управления атаками
    AttackStatisticsViewSet,  # ViewSet для статистики
    SystemConfigViewSet,  # ViewSet для настроек системы
    UserRegistrationView,  # View для регистрации пользователя
    LoginView,  # View для входа пользователя
    LogoutView,  # View для выхода пользователя
    RefreshTokenView,  # View для обновления JWT токена
    CurrentUserView,  # View для получения данных текущего пользователя
    LiveAttacksView,  # View для потоковой передачи атак в реальном времени
    GeoLocationView,  # View для получения геолокации по IP
    DashboardStatsView,  # View для статистики дашборда
)

# Создаем роутер для автоматической регистрации ViewSet
router = DefaultRouter()

# Регистрируем ViewSet с соответствующими basename
router.register(r'attacks', CyberAttackViewSet, basename='attack')  # /api/attacks/
router.register(r'statistics', AttackStatisticsViewSet, basename='statistics')  # /api/statistics/
router.register(r'config', SystemConfigViewSet, basename='config')  # /api/config/

# Основные URL паттерны API
urlpatterns = [
    # Включаем автоматически сгенерированные роутером URL
    path('', include(router.urls)),
    
    # Эндпоинты аутентификации
    path('auth/register/', UserRegistrationView.as_view(), name='auth-register'),  # POST /api/auth/register/ - регистрация
    path('auth/login/', LoginView.as_view(), name='auth-login'),  # POST /api/auth/login/ - вход
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),  # POST /api/auth/logout/ - выход
    path('auth/refresh/', RefreshTokenView.as_view(), name='auth-refresh'),  # POST /api/auth/refresh/ - обновление токена
    path('auth/me/', CurrentUserView.as_view(), name='auth-me'),  # GET /api/auth/me/ - текущий пользователь
    
    # Дополнительные эндпоинты
    path('live/', LiveAttacksView.as_view(), name='live-attacks'),  # GET /api/live/ - атаки в реальном времени
    path('geo/', GeoLocationView.as_view(), name='geo-location'),  # GET /api/geo/?ip=x.x.x.x - геолокация
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),  # GET /api/dashboard/ - статистика дашборда
]
