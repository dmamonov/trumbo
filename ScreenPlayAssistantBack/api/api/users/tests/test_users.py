"""Users tests."""

# Django
from rest_framework.test import APITestCase
from rest_framework import status
from django.conf import settings

# Models
from api.users.models import User
from api.authentication.models import ExternalToken

# Utils
from api.authentication.enums import ExternalTokenType
from api.users.enums import SetUpStatus, PasswordStatus
from api.users.factories import UserFactory
from api.utils.tests import DefaultTestHelper, response_error
from api.users.roles import UserRoles
from api.authentication.enums import ExternalTokenChannel

# Users helper


class UserTestHelper(DefaultTestHelper):
    default_path = 'users'
    model_class = User
    factory = UserFactory
    sample_data = {
        'default': {
            'role': UserRoles.STANDARD,
            'is_active': True,
        },
        'super_admin': {
            'role': UserRoles.ADMIN,
            'is_active': True,
        },
        'john_doe': {
            'dob': '2000-01-01',
            'password': 'SecurePassword#1',
            'setup_status': SetUpStatus.VALIDATED,
            'is_active': True,
            'role': UserRoles.STANDARD,
        },
    }

    create_path = '/'+settings.API_URI+'/auth/sign-up/'
    signup_validate_path = '/'+settings.API_URI+'/auth/sign-up-validate/'
    auth_path = '/'+settings.API_URI+'/auth/token/'
    refresh_path = '/'+settings.API_URI+'/auth/token/refresh/'

    @classmethod
    def force_create(cls, client=None, data={}, sample_name='default', force_auth=False):
        # Create new Object with the given data
        sample = cls._get_data(data, sample_name)
        pwd = sample.pop('password', None)
        obj = cls.factory(**sample)
        if pwd:
            obj.set_password(pwd)
            obj.save()

        if force_auth:
            if not client:
                raise Exception('for force auth, client is required')
            client.force_authenticate(user=obj)

        return obj

    @classmethod
    @response_error
    def signup_1_step(cls, client, data=None, sample_name='default'):
        data = cls._get_data(data, sample_name)
        return client.post(cls.create_path, data, format='json')

    @classmethod
    @response_error
    def signup_validate_2_step(cls, client, data=None, sample_name='default'):
        data = cls._get_data(data, sample_name)
        return client.post(cls.signup_validate_path, data, format='json')

    @classmethod
    @response_error
    def update(cls, client, data=None, sample_name='default', headers=None):
        data = cls._get_data(data, sample_name)
        return client.patch(cls.signup_update_path, data, format='json', headers=headers)

    @classmethod
    @response_error
    def auth(cls, client, data=None):
        return client.post(cls.auth_path, data, format='json')

    @classmethod
    @response_error
    def refresh(cls, client, data=None):
        return client.post(cls.refresh_path, data, format='json')


class AdminUserPostApiTestCase(APITestCase):

    def test_endpoint_responses_code(self):
        user_data = UserTestHelper.get_sample_data('john_doe')
        user = UserTestHelper.force_create(self.client, data=user_data)
        auth_request = UserTestHelper.auth(self.client, data=dict(
            phone_number=user.phone_number, password=user_data['password']))
        self.assertEqual(auth_request.status_code, status.HTTP_200_OK)

        retrieve_request = UserTestHelper.refresh(
            self.client, data=dict(refresh=auth_request.data[settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']]))
        self.assertEqual(retrieve_request.status_code, status.HTTP_200_OK)

    def test_object_creation(self):
        phone_number = "+123456789"
        start_count = UserTestHelper.non_deleted_objects_count()

        UserTestHelper.signup_1_step(
            self.client, data=dict(
                phone_number=phone_number,
                channel=ExternalTokenChannel.CONSOLE.label,
            ))
        self.assertEqual(
            UserTestHelper.non_deleted_objects_count(), start_count+1)

        external_tokens = ExternalToken.get_phone_valid_tokens(
            phone_number, ExternalTokenType.VALIDATE_ACCOUNT)
        self.assertTrue(bool(external_tokens))

        auth_credentials = dict(
            phone_number=phone_number,
            token=external_tokens.first().token,
        )
        validation_request = UserTestHelper.signup_validate_2_step(
            self.client, data=auth_credentials)
        self.assertEqual(validation_request.status_code, status.HTTP_200_OK)

        update_request = UserTestHelper.partially_update(
            self.client, 'current', data=auth_credentials, headers=validation_request.data)
        self.assertEqual(update_request.status_code, status.HTTP_200_OK)
