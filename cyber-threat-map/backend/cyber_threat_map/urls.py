"""
URL конфигурация основного проекта Django.
Определяет маршруты для всего приложения включая API и административную панель.
"""

from django.contrib import admin  # Импортируем административную панель Django
from django.urls import path, include  # Импортируем функции для работы с URL
from django.conf import settings  # Импортируем настройки Django
from django.conf.urls.static import static  # Импортируем функцию для обработки статических файлов

# Определяем основные URL паттерны проекта
urlpatterns = [
    # Административная панель Django (доступна только для суперпользователей)
    path('admin/', admin.site.urls),
    
    # API endpoints для карты киберугроз
    # Все API запросы будут иметь префикс /api/
    path('api/', include('api.urls')),
    
    # Аутентификация через Django REST Framework (браузерная)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Добавляем обработку статических файлов в режиме отладки (DEBUG=True)
# В продакшене статические файлы должен обслуживать веб-сервер (nginx, apache)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Заголовки для документации API
admin.site.site_header = "Карта Киберугроз - Администрирование"
admin.site.site_title = "Карта Киберугроз Admin"
admin.site.index_title = "Панель управления системой безопасности"
