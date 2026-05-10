"""
Конфигурация URL маршрутов Django проекта.
Определяет основные пути к API, админ-панели и другим эндпоинтам.
"""

from django.contrib import admin  # Импорт административной панели Django
from django.urls import path, include  # Импорт функций для определения URL паттернов
from django.http import JsonResponse  # Импорт для возврата JSON ответов
from rest_framework.decorators import api_view, permission_classes  # Декораторы для API view
from rest_framework.permissions import AllowAny  # Разрешение для публичного доступа


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Корневой эндпоинт API.
    Возвращает информацию о доступных эндпоинтах и версии API.
    
    Args:
        request: HTTP запрос
        
    Returns:
        JSON ответ с информацией об API
    """
    return JsonResponse({
        'message': 'Добро пожаловать в API Карты Киберугроз',  # Приветственное сообщение
        'version': '1.0.0',  # Версия API
        'endpoints': {  # Список доступных эндпоинтов
            'attacks': '/api/attacks/',  # Эндпоинт для списка атак
            'statistics': '/api/statistics/',  # Эндпоинт для статистики
            'auth': '/api/auth/',  # Эндпоинт для аутентификации
            'admin': '/admin/',  # Административная панель
        },
        'docs': '/api/docs/',  # Документация API (если доступна)
    })


# Основные URL паттерны проекта
urlpatterns = [
    # Административная панель Django по адресу /admin/
    path('admin/', admin.site.urls),
    
    # API приложение по префиксу /api/
    # Все маршруты из api/urls.py будут доступны с префиксом /api/
    path('api/', include('api.urls')),
    
    # Корневой путь возвращает информацию об API
    path('', api_root, name='api-root'),
    
    # API браузер DRF для удобного просмотра API (только в режиме отладки)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
