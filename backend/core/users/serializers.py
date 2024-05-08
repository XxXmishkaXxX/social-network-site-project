from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email


class CustomLoginSerializer(LoginSerializer):
    username = None
