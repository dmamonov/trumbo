
# Rest Framework
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

# models
from api.users.models import User
from api.authentication.models import ExternalToken
from api.authentication.enums import ExternalTokenType

# Serializers
from api.authentication.serializers import *
from api.authentication.services import signup, authentication, jwt_authentication
from api.utils.decorators import validate_data

# Persmissions
from rest_framework.permissions import AllowAny

# Utilities
from django.conf import settings


class SignupViewSet(GenericViewSet):

    @action(detail=False, methods=['post'], serializer_class=SignUpRequestCodeSerializer, permission_classes=[
        AllowAny
    ], name='sign-up', url_path='sign-up')
    @validate_data()
    def sign_up(self, request, validated_data):
        result = signup.signup_request_code(**validated_data)
        return dict(data=result)

    @action(detail=False, methods=['post'], serializer_class=SignUpValidateCodeSerializer, permission_classes=[
        AllowAny
    ], name='sign-up-validate', url_path='sign-up-validate')
    @validate_data()
    def sign_up_validate(self, request, validated_data):

        user = validated_data.pop('user')
        signup.signup_validated(user=user)

        response = Response(status=200)
        jwt_tokens = jwt_authentication.django_user_jwt(user)
        jwt = authentication.user_jwt_setting(
            response.set_cookie, settings.SIMPLE_JWT, refresh_token=jwt_tokens['refresh'], access_token=jwt_tokens['access'])
        response.data = jwt
        return response

    @action(detail=False, methods=['post'], serializer_class=ForgotPasswordValidateCodeSerializer, permission_classes=[
        AllowAny
    ], name='forgot-password-validate', url_path='forgot-password-validate')
    @validate_data()
    def forgot_password_validate(self, request, validated_data):
        user = validated_data.pop('user')
        signup.forgot_password_validated(
            user=user
        )
        response = Response(status=200)
        jwt_tokens = jwt_authentication.django_user_jwt(user)
        jwt = authentication.user_jwt_setting(
            response.set_cookie, settings.SIMPLE_JWT, refresh_token=jwt_tokens['refresh'], access_token=jwt_tokens['access'])
        response.data = jwt
        return response

    @action(detail=False, methods=['post'], serializer_class=ForgotPasswordRequestCodeSerializer, permission_classes=[
        AllowAny
    ], name='forgot-password', url_path='forgot-password')
    @validate_data()
    def forgot_password(self, request, validated_data):
        result = signup.forgot_password_request_code(
            **validated_data)
        return dict(data=result)
