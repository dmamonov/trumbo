# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from api.events.views import *

router = DefaultRouter()

router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls))
]
