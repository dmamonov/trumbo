# User serializers

# Rest Framework
from rest_framework import serializers

# Django
from django.contrib.auth.models import Group

# Models
from api.users.models import User
from api.users.enums import SetUpStatus, PasswordStatus

# Serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'dob', 'phone_number', 'public', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': False}
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password_status'] = PasswordStatus.ACTIVE
            instance.set_password(validated_data.pop('password'))

        if not instance.setup_status != SetUpStatus.VALIDATED:
            if instance.password and instance.username and instance.phone_number:
                instance.setup_status = SetUpStatus.VALIDATED

        if instance.first_sign_up == True:
            instance.first_sign_up = False

        return super().update(instance, validated_data)


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class Auth0CreateUserSerializer(serializers.ModelSerializer):
    token = serializers.DictField(write_only=True)

    class Meta:
        model = User
        fields = ['token']

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        data = validated_data['token']
        auth0_id = data['sub'].split('|')[1]
        generated_email = False
        username = str(data['nickname']).replace(" ", ".")

        # generate fake email for providers that do not
        # send it
        if 'email' not in data:
            data['email'] = f"{auth0_id}@auto_generated.email"
            generated_email = True

        if User.objects.filter(username=username).exists() or username == "":
            username += auth0_id

        user_data = dict(
            email=data['email'],
            username=username,
            auth0_id=auth0_id,
            setup_status=SetUpStatus.VALIDATED,
            password_status=PasswordStatus.EXTERNAL,
            generated_email=generated_email,
        )
        user = User.objects.create_user(**user_data)
        return user
