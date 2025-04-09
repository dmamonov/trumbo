
# Factories
from api.users.factories.user import UserFactory

# Utilities
import factory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'posts.Post'
        django_get_or_create = ('content', 'created_by')

    content = factory.Faker('paragraph', nb_sentences=4)

    created_by = factory.SubFactory(UserFactory)
