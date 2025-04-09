# Django
from django.urls import include, path, re_path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from api.cms.views import *

router = DefaultRouter()

router.register(r'cms', CMSViewSet, basename='cms')

urlpatterns = [
    path('', include(router.urls)),
]
