""" User model."""

# Django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Utilities
from api.utils.models import BaseModel
from api.users.roles import UserRoles
from api.users.enums import SetUpStatus, PasswordStatus
from django.utils.translation import gettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))

        if not username:
            username = email
        user = self.model(email=email, username=username, **extra_fields)
        if not password:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email=email, password=password, username=email, **extra_fields)


class User(BaseModel, AbstractUser):
    """
    User model

    Extends from Django's Abstract User and add some extra fields
    """

    class Meta:
        permissions = (
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(max_length=152, blank=True)

    last_name = models.CharField(max_length=152, blank=True)

    email = models.EmailField(unique=True)

    dob = models.DateField(null=True)

    phone_number = models.CharField(max_length=16, null=True)

    setup_status = models.IntegerField(
        choices=SetUpStatus.choices, default=SetUpStatus.SIGN_UP_VALIDATION)

    password_status = models.IntegerField(
        choices=PasswordStatus.choices, default=PasswordStatus.CHANGE)

    preferred_language_code = models.CharField(max_length=16, default='en_US')

    role = models.CharField(choices=UserRoles.choices,
                            max_length=5, blank=True, null=True)

    public = models.BooleanField(default=False)

    objects = UserManager()

    generated_email = models.BooleanField(default=False)

    first_sign_up = models.BooleanField(default=True)

    auth0_id = models.CharField(
        default='', max_length=100, blank=True, null=True)

    def get_owner(self):
        return self

    def can_modify(self, user, attributes=[]):
        print("attributes", attributes)
        has_model_access = self.get_owner() == user
        if not has_model_access:
            return False
        if 'password' in attributes:
            if self.password_status != PasswordStatus.CHANGE:
                return False
        return True

    def is_public(self):
        return self.public

    def is_app_superuser(self):
        return self.role == UserRoles.ADMIN

    def can_auth(self):
        if self.setup_status in [SetUpStatus.SIGN_UP_VALIDATION.value]:
            print("WARNING: can't login because",
                  "setup_status", self.setup_status)
            return False
        if self.password_status in [PasswordStatus.EXTERNAL.value]:
            print("WARNING: can't login because",
                  "password_status", self.password_status)
            return False
        return True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
