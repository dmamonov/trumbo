"""
Authentication Views
"""

# Rest Framework
from rest_framework.response import Response
from rest_framework import status

# Serializers
from api.authentication.serializers import *

# Services
from api.authentication.services import signup, authentication, jwt_authentication

# Utilities
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from api.utils.decorators import validate_data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        response = Response(status=status.HTTP_200_OK)
        tokens = dict(
            refresh_token=serializer.validated_data['refresh'],
            access_token=serializer.validated_data['access'],
        )
        response.data = authentication.user_jwt_setting(response.set_cookie, settings.SIMPLE_JWT, is_refresh=False, **tokens)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        response = Response(status=status.HTTP_200_OK)
        tokens = dict(
            access_token=serializer.validated_data['access'],
        )
        response.data = authentication.user_jwt_setting(response.set_cookie, settings.SIMPLE_JWT, is_refresh=True, **tokens)
        return response
