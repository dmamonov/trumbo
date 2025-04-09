"""Authentication serializers"""

# Serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import serializers
from django.conf import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.can_auth():
            raise serializers.ValidationError(dict(user="you can not log in"))
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # if you are using double authentication this maybe needed
        # data['username'] = str(self.user.username)

        # Add extra responses here
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh_token = self.context['request'].COOKIES.get(
            settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']) or None
        if not attrs['refresh'] and refresh_token:
            attrs['refresh'] = refresh_token
        try:
            data = super().validate(attrs)
        except TokenError:
            raise serializers.ValidationError(
                dict(refresh="invalid refresh token or has expired"))
        return data
