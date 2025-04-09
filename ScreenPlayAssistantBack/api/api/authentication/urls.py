# Django
from django.urls import include, path
from django.contrib.auth import views as auth_view

# Django Rest Framework
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Views
from .views import *

router = DefaultRouter()

# router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'auth', SignupViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    # path('password-reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(),name='password-reset'),
    # path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(),name='password-reset-complete'),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
]
