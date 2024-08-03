from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
    TokenVerifySerializer
from django.conf import settings as django_settings
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken
from .models import User, ChatMessage, Chat
from rest_framework import serializers

####### АВТОРИЗАЦИЯ #######

# register
class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token', 'username')

    def get_token(self, obj):
        access_token = AccessToken.for_user(obj)
        refresh_token = RefreshToken.for_user(obj)
        return {
            'access': str(access_token),
            'refresh': str(refresh_token),
        }

    # проверка на уникальность email
    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email уже зарегистрирован')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        instance.email = email or instance.email
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# retrieve
class UserRetrieveSerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt.token_blacklist" in django_settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        user = User.objects.get(id=token.payload['user_id'])
        data = {}
        data["id"] = user.id
        data["username"] = user.username
        data["email"] = user.email
        data["phone"] = user.phone
        data["is_telegram_use"] = user.is_telegram_use
        data["telegram_id"] = user.telegram_id
        try:
            # ссылка на фото без домена
            photo_url = user.photo.url
            # ссылка на фото с доменом
            abs_photo_url = self.context['request'].build_absolute_uri(photo_url)
            data['photo'] = abs_photo_url
        except:
            data['photo'] = None

        return data

# update
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'phone',
            'email',
            'photo',
            'is_telegram_use',
            'telegram_id',
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.telegram_id = validated_data.get('telegram_id', instance.telegram_id)
        # если телеграм не пустая строка, то использовал
        instance.is_telegram_use = True if instance.telegram_id else False
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance

# login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        try:
            # ссылка на фото без домена
            photo_url = self.user.photo.url
            # ссылка на фото с доменом
            abs_photo_url = self.context['request'].build_absolute_uri(photo_url)
            data['photo'] = abs_photo_url
        except:
            data['photo'] = None
        return data

# verify
class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt.token_blacklist" in django_settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        user = User.objects.get(id=token.payload['user_id'])
        data = {}
        data["username"] = user.username
        try:
            # ссылка на фото без домена
            photo_url = user.photo.url
            # ссылка на фото с доменом
            abs_photo_url = self.context['request'].build_absolute_uri(photo_url)
            data['photo'] = abs_photo_url
        except:
            data['photo'] = None

        return data

# refresh
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        user = User.objects.get(id=refresh.payload['user_id'])
        data["username"] = user.username
        try:
            # ссылка на фото без домена
            photo_url = user.photo.url
            # ссылка на фото с доменом
            abs_photo_url = self.context['request'].build_absolute_uri(photo_url)
            data['photo'] = abs_photo_url
        except:
            data['photo'] = None

        return data

class UserInfoRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'photo',
        )

class ChatMessageCreateSerializer(serializers.ModelSerializer):
    user_create = UserInfoRetrieveSerializer(read_only=True)
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = [
            'user_create'
        ]

class ChatMessageRetrieveSerializer(serializers.ModelSerializer):
    user_create = UserInfoRetrieveSerializer()
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ChatMessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = [
            'date_time',
            'user_create',
        ]

    def update(self, instance, validated_data):
        # убираем ключи со значениями None из словаря
        for key, value in list(validated_data.items()):
            if value is None:
                del validated_data[key]

        instance.text = validated_data.get('text', instance.text)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance


class ChatSerializer(serializers.ModelSerializer):
    users = UserInfoRetrieveSerializer(many=True)
    messages = ChatMessageRetrieveSerializer(many=True)
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = [
            'users'
        ]

    # исключаем текущего пользователя из выводимого списка пользователей чата
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)

        if request and request.user:
            current_user_id = request.user.id
            data['users'] = [user for user in data['users'] if user['id'] != current_user_id]

        return data

######### КАСТОМИЗАЦИЯ JWT-ТОКЕНОВ #########
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         token['username'] = user.username
#         # ...
#
#         return token