"""
Сериализаторы для преобразования моделей Django в JSON и обратно.
Используется Django REST Framework для API эндпоинтов.
"""

from rest_framework import serializers  # Импортируем сериализаторы DRF
from django.contrib.auth import get_user_model  # Функция для получения модели пользователя
from .models import CyberAttack, AttackStatistics, SystemConfig  # Импортируем модели

# Получаем модель пользователя (может быть кастомной)
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    Преобразует данные пользователя в JSON формат для API.
    """
    
    # Поле для подтверждения пароля (не сохраняется в БД)
    password_confirm = serializers.CharField(write_only=True, required=False)  # Только для записи
    
    class Meta:
        """Мета-настройки сериализатора."""
        model = User  # Модель для сериализации
        fields = [  # Поля которые будут включены в сериализацию
            'id',  # Уникальный идентификатор
            'username',  # Имя пользователя
            'email',  # Email адрес
            'first_name',  # Имя
            'last_name',  # Фамилия
            'is_active',  # Статус активности
            'created_at',  # Дата создания
            'updated_at',  # Дата обновления
            'password',  # Пароль (только для записи)
            'password_confirm',  # Подтверждение пароля
        ]
        extra_kwargs = {  # Дополнительные настройки для полей
            'password': {'write_only': True},  # Пароль только для записи (не возвращается в ответах)
            'created_at': {'read_only': True},  # Дата создания только для чтения
            'updated_at': {'read_only': True},  # Дата обновления только для чтения
        }
    
    def validate(self, data):
        """
        Валидация данных пользователя.
        Проверяет совпадение паролей при создании пользователя.
        
        Args:
            data: Словарь с данными пользователя
            
        Returns:
            Проверенные данные или ошибка валидации
        """
        # Проверяем совпадение паролей если они указаны
        if data.get('password') and data.get('password_confirm'):
            if data['password'] != data['password_confirm']:
                raise serializers.ValidationError({"password": "Пароли не совпадают"})  # Ошибка если пароли разные
        return data  # Возвращаем проверенные данные
    
    def create(self, validated_data):
        """
        Создание нового пользователя.
        Хэширует пароль перед сохранением в базу данных.
        
        Args:
            validated_data: Проверенные данные пользователя
            
        Returns:
            Созданный объект пользователя
        """
        # Извлекаем подтверждение пароля из данных (не нужно для создания)
        validated_data.pop('password_confirm', None)
        
        # Создаем пользователя с хэшированным паролем
        user = User.objects.create_user(
            username=validated_data['username'],  # Имя пользователя
            email=validated_data.get('email', ''),  # Email
            password=validated_data['password'],  # Пароль (автоматически хэшируется)
            first_name=validated_data.get('first_name', ''),  # Имя
            last_name=validated_data.get('last_name', ''),  # Фамилия
            is_active=validated_data.get('is_active', True),  # Активность
        )
        return user  # Возвращаем созданного пользователя


class CyberAttackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели кибератаки.
    Преобразует данные об атаке в JSON формат для API.
    """
    
    # Поле для цвета протокола (вычисляемое, только для чтения)
    protocol_color = serializers.SerializerMethodField(read_only=True)  # Вычисляемое поле
    
    class Meta:
        """Мета-настройки сериализатора."""
        model = CyberAttack  # Модель для сериализации
        fields = '__all__'  # Все поля модели будут включены
    
    def get_protocol_color(self, obj):
        """
        Возвращает цвет для протокола атаки.
        Используется для визуализации на карте.
        
        Args:
            obj: Объект кибератаки
            
        Returns:
            HEX код цвета для данного протокола
        """
        # Словарь цветов для различных протоколов
        colors = {
            'TCP': '#00ff00',  # Зеленый для TCP
            'UDP': '#0000ff',  # Синий для UDP
            'ICMP': '#ff0000',  # Красный для ICMP
            'HTTP': '#ffff00',  # Желтый для HTTP
            'HTTPS': '#00ffff',  # Голубой для HTTPS
            'SSH': '#ff00ff',  # Маджента для SSH
            'FTP': '#ffa500',  # Оранжевый для FTP
            'DNS': '#800080',  # Фиолетовый для DNS
        }
        # Возвращаем цвет или белый по умолчанию
        return colors.get(obj.protocol.upper(), '#ffffff')


class AttackStatisticsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели статистики атак.
    Преобразует агрегированные данные статистики в JSON формат.
    """
    
    class Meta:
        """Мета-настройки сериализатора."""
        model = AttackStatistics  # Модель для сериализации
        fields = '__all__'  # Все поля модели будут включены


class SystemConfigSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели системной конфигурации.
    Позволяет управлять настройками системы через API.
    """
    
    class Meta:
        """Мета-настройки сериализатора."""
        model = SystemConfig  # Модель для сериализации
        fields = '__all__'  # Все поля модели будут включены


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.
    Принимает username и пароль для аутентификации.
    """
    
    username = serializers.CharField(required=True)  # Имя пользователя (обязательное поле)
    password = serializers.CharField(required=True, write_only=True)  # Пароль (обязательное, только для записи)


class RegisterSerializer(serializers.Serializer):
    """
    Сериализатор для регистрации нового пользователя.
    Принимает данные для создания новой учетной записи.
    """
    
    username = serializers.CharField(required=True)  # Имя пользователя (обязательное)
    email = serializers.EmailField(required=True)  # Email (обязательное)
    password = serializers.CharField(required=True, write_only=True)  # Пароль (обязательное, только для записи)
    password_confirm = serializers.CharField(required=True, write_only=True)  # Подтверждение пароля (обязательное)
    
    def validate(self, data):
        """
        Валидация данных регистрации.
        Проверяет совпадение паролей и уникальность username/email.
        
        Args:
            data: Словарь с данными регистрации
            
        Returns:
            Проверенные данные или ошибка валидации
        """
        # Проверяем совпадение паролей
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})
        
        # Проверяем уникальность username
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Пользователь с таким именем уже существует"})
        
        # Проверяем уникальность email
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email уже зарегистрирован"})
        
        return data  # Возвращаем проверенные данные
