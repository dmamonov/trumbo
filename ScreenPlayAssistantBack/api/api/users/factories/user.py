# Utilities
import factory
import random

from api.users.roles import UserRoles
from api.users.enums import SetUpStatus


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email', )

    first_name = factory.Faker('first_name')

    phone_number = factory.Faker('phone_number')

    password = factory.Faker('password')

    public = factory.Faker('boolean')

    last_name = factory.Faker('last_name')

    email = factory.LazyAttribute(
        lambda p: f'{p.first_name}.{p.last_name}@mail.com')

    username = factory.LazyAttribute(lambda p: p.email)

    dob = factory.Faker('date_between')

    role = factory.LazyAttribute(lambda _: random.choice(
        list(UserRoles._value2member_map_.values())))
    
    setup_status = factory.LazyAttribute(lambda _: random.choice(
        list(SetUpStatus._value2member_map_.values())))
