from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class UtilsTest(APITestCase):
    # fixtures = ["foodeo.json", "tenant.json"]

    def setUp(self):
        self.request = HttpRequest()
        self.request.META = {"SERVER_NAME": "example.com", "SERVER_PORT": 8000}

        self.user = User.objects.filter(is_staff=False).first()
        self.create_super_user()
        self.create_token_superuser()
        self.create_token_user()
        self.create_user_token_headers()

    def get_group(self, name="Administrador"):
        self.group = Group.objects.get(name=name)

    def create_token_headers(self):
        self.super_user_token_headers = {'HTTP_AUTHORIZATION': self.super_token}

    def create_user_token_headers(self):
        self.user_token_headers = {'HTTP_AUTHORIZATION': '{}'.format(self.token_user)}

    def create_token_user(self):
        token = AccessToken.for_user(self.user)
        token_total = "Bearer {}".format(token)
        self.token_user = token_total

    def create_token_superuser(self):
        token = AccessToken.for_user(self.super_user)
        token_total = "Bearer {}".format(token)
        self.super_token = token_total

    def create_super_user(self, **kwargs):
        data = {"email": 'admin@mail.com', "password": '123'}
        data.update(kwargs)
        self.super_user = User.objects.create_superuser(**data)

    def create_image(self, storage, filename, mode='RGB', size=(100, 100), format="PNG"):
        data = BytesIO()
        Image.new(mode=mode, size=size).save(data, format)
        data.seek(0)
        if not storage:
            return data
        imageFile = ContentFile(data.read())
        image = storage.save(filename, imageFile)
        file = SimpleUploadedFile("{}.{}".format(filename, format), image.getvalue())
        return file
