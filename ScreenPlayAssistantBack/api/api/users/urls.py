# Django
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_view

# Django Rest Framework
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Views
from api.users.views import UsersViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
