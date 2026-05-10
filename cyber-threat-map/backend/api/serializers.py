"""
Сериализаторы Django REST Framework для приложения карты киберугроз.
Преобразуют модели данных в JSON формат и обратно.
"""

from rest_framework import serializers  # Импорт сериализаторов DRF
from api.models import User, CyberAttack, AttackStatistics, SystemConfig  # Импорт моделей
from django.contrib.auth import get_user_model  # Функция получения модели пользователя


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    Используется для регистрации, просмотра и обновления пользователей.
    """
    
    class Meta:
        """Мета-настройки сериализатора User."""
        model = User  # Модель которую сериализуем
        fields = [
            'id',  # Уникальный идентификатор пользователя
            'username',  # Имя пользователя (логин)
            'email',  # Email адрес
            'first_name',  # Имя
            'last_name',  # Фамилия
            'is_active',  # Статус активности
            'created_at',  # Дата создания
            'updated_at',  # Дата обновления
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']  # Поля только для чтения


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    Включает поля для пароля с дополнительной валидацией.
    """
    password = serializers.CharField(
        write_only=True,  # Поле только для записи (не возвращается в ответах)
        required=True,  # Обязательное поле
        style={'input_type': 'password'},  # Тип ввода пароль
        help_text='Пароль должен содержать минимум 8 символов'  # Подсказка для пользователя
    )
    password_confirm = serializers.CharField(
        write_only=True,  # Поле только для записи
        required=True,  # Обязательное поле
        style={'input_type': 'password'},  # Тип ввода пароль
        help_text='Подтверждение пароля'  # Подсказка
    )

    class Meta:
        """Мета-настройки сериализатора регистрации."""
        model = User  # Модель пользователя
        fields = [
            'username',  # Имя пользователя
            'email',  # Email
            'password',  # Пароль
            'password_confirm',  # Подтверждение пароля
        ]

    def validate_password(self, value):
        """
        Валидация пароля: проверка минимальной длины.
        
        Args:
            value: Значение пароля
            
        Returns:
            Проверенный пароль
            
        Raises:
            serializers.ValidationError: Если пароль слишком короткий
        """
        if len(value) < 8:
            raise serializers.ValidationError('Пароль должен содержать минимум 8 символов')
        return value

    def validate(self, data):
        """
        Общая валидация данных: проверка совпадения паролей.
        
        Args:
            data: Словарь с данными формы
            
        Returns:
            Проверенные данные
            
        Raises:
            serializers.ValidationError: Если пароли не совпадают
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают'})
        return data

    def create(self, validated_data):
        """
        Создание нового пользователя с хешированием пароля.
        
        Args:
            validated_data: Проверенные данные без password_confirm
            
        Returns:
            Созданный объект пользователя
        """
        # Удаляем поле подтверждения пароля из данных
        validated_data.pop('password_confirm')
        
        # Создаем пользователя с хешированным паролем
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class CyberAttackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели кибератаки.
    Преобразует данные атаки в JSON формат для API.
    """
    severity_display = serializers.SerializerMethodField()  # Поле для отображения уровня опасности
    firewall_action_display = serializers.SerializerMethodField()  # Поле для отображения действия фаервола

    class Meta:
        """Мета-настройки сериализатора CyberAttack."""
        model = CyberAttack  # Модель которую сериализуем
        fields = [
            'id',  # Уникальный идентификатор атаки
            'source_ip',  # IP адрес источника
            'target_ip',  # IP адрес цели
            'source_port',  # Порт источника
            'target_port',  # Порт цели
            'protocol',  # Протокол
            'attack_type',  # Тип атаки
            'vulnerability_type',  # Тип уязвимости
            'country',  # Страна
            'city',  # Город
            'latitude',  # Широта
            'longitude',  # Долгота
            'timestamp',  # Время атаки
            'severity',  # Уровень опасности (код)
            'severity_display',  # Уровень опасности (текст)
            'firewall_action',  # Действие фаервола (код)
            'firewall_action_display',  # Действие фаервола (текст)
            'raw_log',  # Исходный лог
            'created_at',  # Дата создания записи
            'updated_at',  # Дата обновления записи
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']  # Поля только для чтения

    def get_severity_display(self, obj):
        """
        Получение человекочитаемого названия уровня опасности.
        
        Args:
            obj: Объект CyberAttack
            
        Returns:
            Текстовое представление уровня опасности
        """
        severity_choices = dict(CyberAttack._meta.get_field('severity').choices)
        return severity_choices.get(obj.severity, obj.severity)

    def get_firewall_action_display(self, obj):
        """
        Получение человекочитаемого названия действия фаервола.
        
        Args:
            obj: Объект CyberAttack
            
        Returns:
            Текстовое представление действия фаервола
        """
        action_choices = dict(CyberAttack._meta.get_field('firewall_action').choices)
        return action_choices.get(obj.firewall_action, obj.firewall_action)


class AttackStatisticsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели статистики атак.
    Возвращает агрегированные данные за период.
    """
    class Meta:
        """Мета-настройки сериализатора AttackStatistics."""
        model = AttackStatistics  # Модель которую сериализуем
        fields = [
            'id',  # Уникальный идентификатор
            'date',  # Дата статистики
            'top_attack_types',  # Топ типов атак
            'top_vulnerabilities',  # Топ уязвимостей
            'top_ports',  # Топ портов
            'top_countries',  # Топ стран
            'total_attacks',  # Всего атак
            'unique_sources',  # Уникальных источников
            'created_at',  # Дата создания
            'updated_at',  # Дата обновления
        ]
        read_only_fields = fields  # Все поля только для чтения


class SystemConfigSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели системных настроек.
    Позволяет управлять конфигурацией через API.
    """
    class Meta:
        """Мета-настройки сериализатора SystemConfig."""
        model = SystemConfig  # Модель которую сериализуем
        fields = [
            'id',  # Уникальный идентификатор
            'key',  # Ключ настройки
            'value',  # Значение настройки
            'description',  # Описание
            'updated_at',  # Дата обновления
        ]
        read_only_fields = ['id', 'updated_at']  # Поля только для чтения


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.
    Принимает username/email и пароль, возвращает JWT токены.
    """
    username = serializers.CharField(required=False, allow_blank=True)  # Имя пользователя (необязательно)
    email = serializers.EmailField(required=False, allow_blank=True)  # Email (необязательно)
    password = serializers.CharField(write_only=True, required=True)  # Пароль (обязательно)

    def validate(self, data):
        """
        Валидация учетных данных пользователя.
        
        Args:
            data: Словарь с username/email и password
            
        Returns:
            Данные с добавленным пользователем
            
        Raises:
            serializers.ValidationError: Если credentials неверны
        """
        from django.contrib.auth import authenticate  # Импорт функции аутентификации
        
        # Определяем поле для аутентификации (username или email)
        username = data.get('username')
        email = data.get('email')
        
        if not username and not email:
            raise serializers.ValidationError('Необходимо указать username или email')
        
        # Если указан email, используем его для поиска пользователя
        if email:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError('Неверный email или пароль')
        
        # Аутентифицируем пользователя
        user = authenticate(username=username, password=data['password'])
        
        if not user:
            raise serializers.ValidationError('Неверное имя пользователя или пароль')
        
        if not user.is_active:
            raise serializers.ValidationError('Учетная запись deactivated')
        
        # Добавляем пользователя в данные для использования во view
        data['user'] = user
        return data
