"""
Представления (Views) Django REST Framework для API карты киберугроз.
Обрабатывают HTTP запросы и возвращают данные в формате JSON.
"""

from rest_framework import viewsets, status  # Импорт базовых классов DRF
from rest_framework.decorators import api_view, permission_classes  # Декораторы для function-based views
from rest_framework.response import Response  # Класс для формирования ответов
from rest_framework.permissions import IsAuthenticated, AllowAny  # Классы разрешений
from rest_framework.views import APIView  # Базовый класс для class-based views
from rest_framework_simplejwt.tokens import RefreshToken  # Класс для работы с JWT токенами
from django.contrib.auth import login, logout  # Функции аутентификации Django
from django.db.models import Count, Q  # Агрегатные функции и условия для запросов к БД
from django.utils import timezone  # Утилиты для работы с временем
from datetime import timedelta  # Класс для работы с интервалами времени
import logging  # Модуль для логгирования

# Импортируем модели и сериализаторы
from api.models import CyberAttack, AttackStatistics, SystemConfig, User
from api.serializers import (
    CyberAttackSerializer,
    AttackStatisticsSerializer,
    SystemConfigSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
)
from api.log_parser import LogParser, get_protocol_color  # Парсер логов и функция получения цвета протокола

# Настройка логгера для модуля views
logger = logging.getLogger(__name__)


class CyberAttackViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления кибератаками.
    Предоставляет CRUD операции (Create, Retrieve, Update, Delete) и фильтрацию.
    """
    queryset = CyberAttack.objects.all()  # Все записи атак из базы данных
    serializer_class = CyberAttackSerializer  # Сериализатор для преобразования данных
    permission_classes = [IsAuthenticated]  # Требуется аутентификация для всех операций
    
    # Поля по которым можно искать через ?search=...
    search_fields = [
        'source_ip',  # Поиск по IP источника
        'target_ip',  # Поиск по IP цели
        'attack_type',  # Поиск по типу атаки
        'country',  # Поиск по стране
        'protocol',  # Поиск по протоколу
    ]
    
    # Поля по которым можно фильтровать через ?field=value
    filterset_fields = [
        'protocol',  # Фильтр по протоколу
        'severity',  # Фильтр по уровню опасности
        'firewall_action',  # Фильтр по действию фаервола
        'country',  # Фильтр по стране
    ]
    
    # Поля для сортировки через ?ordering=-timestamp
    ordering_fields = ['timestamp', 'created_at', 'severity']
    ordering = ['-timestamp']  # Сортировка по умолчанию: новые атаки первыми

    def get_queryset(self):
        """
        Переопределение queryset для фильтрации по параметрам запроса.
        
        Returns:
            Отфильтрованный queryset атак
        """
        queryset = super().get_queryset()
        
        # Получаем параметры даты из запроса
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        # Фильтруем по диапазону дат если указаны
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        # Фильтруем по уровню опасности
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        return queryset


class AttackStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet только для чтения статистики атак.
    Предоставляет доступ к агрегированным данным.
    """
    queryset = AttackStatistics.objects.all()  # Все записи статистики
    serializer_class = AttackStatisticsSerializer  # Сериализатор статистики
    permission_classes = [IsAuthenticated]  # Требуется аутентификация


class SystemConfigViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления системными настройками.
    Только для администраторов.
    """
    queryset = SystemConfig.objects.all()  # Все настройки системы
    serializer_class = SystemConfigSerializer  # Сериализатор настроек
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get_permissions(self):
        """
        Переопределение разрешений: только администраторы могут изменять настройки.
        
        Returns:
            Список экземпляров классов разрешений
        """
        if self.action in ['list', 'retrieve']:
            # Просмотр доступен всем авторизованным
            return [IsAuthenticated()]
        # Создание, изменение, удаление только для администраторов
        return [IsAuthenticated()]


class UserRegistrationView(APIView):
    """
    Представление для регистрации нового пользователя.
    Принимает POST запрос с данными пользователя.
    """
    permission_classes = [AllowAny]  # Регистрация доступна без аутентификации

    def post(self, request):
        """
        Обработка POST запроса на регистрацию.
        
        Args:
            request: HTTP запрос с данными регистрации
            
        Returns:
            Response с данными пользователя или ошибками валидации
        """
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Создаем пользователя
            user = serializer.save()
            
            # Генерируем JWT токены
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,  # Данные пользователя
                'refresh': str(refresh),  # Refresh токен
                'access': str(refresh.access_token),  # Access токен
                'message': 'Пользователь успешно зарегистрирован'
            }, status=status.HTTP_201_CREATED)
        
        # Возвращаем ошибки валидации
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Представление для входа пользователя.
    Принимает username/email и пароль, возвращает JWT токены.
    """
    permission_classes = [AllowAny]  # Вход доступен без аутентификации

    def post(self, request):
        """
        Обработка POST запроса на вход.
        
        Args:
            request: HTTP запрос с credentials
            
        Returns:
            Response с токенами или ошибкой
        """
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Выполняем вход в систему
            login(request, user)
            
            # Генерируем JWT токены
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Вход выполнен успешно'
            })
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Представление для выхода пользователя.
    Blacklist-ит refresh токен.
    """
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def post(self, request):
        """
        Обработка POST запроса на выход.
        
        Args:
            request: HTTP запрос
            
        Returns:
            Response с подтверждением выхода
        """
        try:
            # Получаем refresh токен из тела запроса
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Необходимо предоставить refresh токен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist-им токен (если настроено)
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Выполняем выход
            logout(request)
            
            return Response({'message': 'Выход выполнен успешно'})
        except Exception as e:
            logger.error(f"Ошибка при выходе: {e}")
            return Response(
                {'error': 'Ошибка при выходе'},
                status=status.HTTP_400_BAD_REQUEST
            )


class RefreshTokenView(APIView):
    """
    Представление для обновления access токена.
    Использует refresh токен для генерации новой пары токенов.
    """
    permission_classes = [AllowAny]  # Обновление токена доступно без аутентификации

    def post(self, request):
        """
        Обработка POST запроса на обновление токена.
        
        Args:
            request: HTTP запрос с refresh токеном
            
        Returns:
            Response с новыми токенами
        """
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Необходимо предоставить refresh токен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Создаем новый refresh токен из старого
            refresh = RefreshToken(refresh_token)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except Exception as e:
            logger.error(f"Ошибка обновления токена: {e}")
            return Response(
                {'error': 'Неверный refresh токен'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class CurrentUserView(APIView):
    """
    Представление для получения данных текущего пользователя.
    """
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get(self, request):
        """
        GET запрос для получения данных текущего пользователя.
        
        Args:
            request: HTTP запрос
            
        Returns:
            Response с данными пользователя
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LiveAttacksView(APIView):
    """
    Представление для получения последних атак в реальном времени.
    Используется для обновления карты.
    """
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get(self, request):
        """
        GET запрос для получения последних N атак.
        
        Args:
            request: HTTP запрос с параметром limit
            
        Returns:
            Response со списком атак
        """
        # Получаем лимит записей (по умолчанию 50)
        limit = int(request.query_params.get('limit', 50))
        
        # Получаем последние атаки
        attacks = CyberAttack.objects.all()[:limit]
        
        # Сериализуем данные
        serializer = CyberAttackSerializer(attacks, many=True)
        
        return Response({
            'count': attacks.count(),
            'results': serializer.data,
        })


class GeoLocationView(APIView):
    """
    Представление для получения геолокации по IP адресу.
    """
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get(self, request):
        """
        GET запрос для получения геоданных по IP.
        
        Args:
            request: HTTP запрос с параметром ip
            
        Returns:
            Response с геоданными
        """
        ip_address = request.query_params.get('ip')
        
        if not ip_address:
            return Response(
                {'error': 'Необходимо указать IP адрес'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # В реальной реализации здесь будет запрос к GeoIP базе
        # Для демонстрации возвращаем фиктивные данные
        return Response({
            'ip': ip_address,
            'country': 'Russia',
            'city': 'Moscow',
            'latitude': 55.7558,
            'longitude': 37.6173,
        })


class DashboardStatsView(APIView):
    """
    Представление для получения сводной статистики дашборда.
    """
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get(self, request):
        """
        GET запрос для получения статистики.
        
        Args:
            request: HTTP запрос
            
        Returns:
            Response со статистикой
        """
        # Период по умолчанию - последние 24 часа
        hours = int(request.query_params.get('hours', 24))
        time_threshold = timezone.now() - timedelta(hours=hours)
        
        # Общее количество атак за период
        total_attacks = CyberAttack.objects.filter(
            timestamp__gte=time_threshold
        ).count()
        
        # Количество уникальных источников
        unique_sources = CyberAttack.objects.filter(
            timestamp__gte=time_threshold
        ).values('source_ip').distinct().count()
        
        # Топ-5 стран по количеству атак
        top_countries = CyberAttack.objects.filter(
            timestamp__gte=time_threshold
        ).exclude(country='').values('country').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Топ-5 протоколов
        top_protocols = CyberAttack.objects.filter(
            timestamp__gte=time_threshold
        ).values('protocol').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Топ-5 типов атак
        top_attack_types = CyberAttack.objects.filter(
            timestamp__gte=time_threshold
        ).values('attack_type').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Распределение по уровням опасности
        severity_distribution = CyberAttack.objects.filter(
            timestamp__gte=time_threshold
        ).values('severity').annotate(
            count=Count('id')
        )
        
        return Response({
            'period_hours': hours,
            'total_attacks': total_attacks,
            'unique_sources': unique_sources,
            'top_countries': list(top_countries),
            'top_protocols': list(top_protocols),
            'top_attack_types': list(top_attack_types),
            'severity_distribution': list(severity_distribution),
            'timestamp': timezone.now().isoformat(),
        })
