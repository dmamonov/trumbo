
# Models
from api.screenplays.models import *

# Utilities
from api.users.permissions import IsAdminPermission, CanCrudPermission, IsSupportReadOnlyPermission
# from rest_framework import permissions

# Rest framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Serializers
from api.screenplays.serializers import ScreenPlaySerializer
from api.utils.views import BaseViewSet

class ScreenPlaysViewSet(BaseViewSet, viewsets.ModelViewSet):
    
    model = ScreenPlay
    serializer_class = ScreenPlaySerializer
    queryset = ScreenPlay.objects.filter(deleted=False)
    # permission_classes = [HasGroupAccess, IsAuthenticated]
    
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset()
