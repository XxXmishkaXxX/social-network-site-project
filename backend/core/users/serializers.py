from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import re

User = get_user_model()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    code = serializers.UUIDField()

class PasswordResetCompleteSerializer(serializers.Serializer):
    uid = serializers.CharField()
    code = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают")
        
        password = data.get('new_password')

        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[\W_]).{8,}$', password):
            raise serializers.ValidationError("Пароль должен содержать только латинские символы и быть не короче 8 символов")
        
        return data

class CustomRegisterSerializer(RegisterSerializer):
    username = None

    domains = ['mail.ru', 'gmail.com', 'yandex.ru']

    def validate_email(self, email):
        
        if email.split('@')[1] not in self.domains:
            raise serializers.ValidationError("Вы использовали не разрешенный почтовый домен.")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с такой почтой уже зарегистрирован или не подтвердил почту.")
        
        return email
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("Пароли не совпадают"))
        return data


class EmailAndPasswordMismatchError(exceptions.ValidationError):
    default_detail = _('Почта или пароль введен неверно')
    default_code = 'email_password_mismatch'

class CustomLoginSerializer(LoginSerializer):
    username = None

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(username=username, email=email, password=password)

        if not user:
            raise EmailAndPasswordMismatchError()

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email=email)

        attrs['user'] = user
        return attrs


