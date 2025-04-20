
# Models
from api.screenplays.models import *

# Utilities
from api.users.permissions import IsAdminPermission, CanCrudPermission, IsSupportReadOnlyPermission
from rest_framework.permissions import AllowAny
# from rest_framework import permissions

# Rest framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Serializers
from api.screenplays.serializers import *
from api.utils.views import BaseViewSet

class ScreenPlaysViewSet(BaseViewSet, viewsets.ModelViewSet):
    
    model = ScreenPlay
    serializer_class = ScreenPlaySerializer
    serializer_classes = dict(
        create=WriteScreenPlaySerializer,
        update=WriteScreenPlaySerializer,
    )
    queryset = ScreenPlay.objects.filter(deleted=False)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset()


class CharacterViewSet(BaseViewSet, viewsets.ModelViewSet):
    
    model = Character
    serializer_class = CharacterSerializer
    serializer_classes = dict(
        create=WriteCharacterSerializer,
        update=WriteCharacterSerializer,
    )
    queryset = Character.objects.filter(deleted=False)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset()


class SceneHighlightViewSet(BaseViewSet, viewsets.ModelViewSet):
    
    model = SceneHighlight
    serializer_class = SceneHighlightSerializer
    serializer_classes = dict(
        create=WriteSceneHighlightSerializer,
        update=WriteSceneHighlightSerializer,
    )
    queryset = SceneHighlight.objects.filter(deleted=False)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset()
