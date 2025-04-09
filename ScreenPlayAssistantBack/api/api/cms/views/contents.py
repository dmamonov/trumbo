
# Models
from api.cms.models import Content

# Serializers
from api.cms.serializers import ContentSerializer

# Utilities
from api.utils.api.views import read_view_from_model
from rest_framework import permissions

"""
# Rest framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Serializers
from api.contents.serializers import ContentSerializer
from api.utils.views import BaseViewSet

class CMSViewSet(BaseViewSet, viewsets.ModelViewSet):
    
    model = Content
    serializer_class = ContentSerializer
    queryset = Content.objects.filter(deleted=False)
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset()
"""

CMSViewSet = read_view_from_model(
    Content,
    serializer_classes={
    'read': ContentSerializer
    },
    permissions=[permissions.AllowAny],
    lookup_field='name',
    search_fields=['name']
)
