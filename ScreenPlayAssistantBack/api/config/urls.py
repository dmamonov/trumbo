"""Main URLs module."""

# Admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# Django
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(title="Screen Play Assistant API Protocol", default_version='v1',
                 description="Screen Play Assistant API Protocol", ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui('swagger',
                                             cache_timeout=0), name='schema-swagger-ui'),
    re_path(settings.API_URI + '/', include('api.users.urls')),
    re_path(settings.API_URI + '/', include('api.events.urls')),
    re_path(settings.API_URI + '/',
            include('api.authentication.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
