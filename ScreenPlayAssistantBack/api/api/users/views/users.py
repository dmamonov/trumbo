# Model Views for users

# Rest framework
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from api.users.models import User

# Serializers
from api.users.serializers import UserSerializer, SimpleUserSerializer

# Permissions
from api.users.permissions import IsAdminPermission, CanCrudPermission

# Utils
from api.utils.pagination import StartEndPagination

# Enums
from api.users.enums import PasswordStatus


class UsersViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    """
    User ViewSet based on role
    """
    serializer_class = UserSerializer
    serializer_classes = dict(
        list=SimpleUserSerializer,
    )
    model = User
    queryset = User.objects.all()
    pagination_class = StartEndPagination
    permission_classes = [IsAdminPermission | CanCrudPermission]

    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs[lookup_url_kwarg] == 'current':
            user = self.request.user
            self.check_object_permissions(self.request, user)
        else:
            user = super().get_object()
        return user

    # @action(detail=False, methods=['get'])
    # def permissions(self, request):
    #     data = request.user.user_permissions.all()
    #     return Response(data)

    @action(detail=True, methods=['post'], name='change-password', url_path='change-password', permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request, **kwargs):
        user = self.get_object()
        user.password_status = PasswordStatus.CHANGE
        user.save()
        print()

        partial = kwargs.pop('partial', False)
        serializer = UserSerializer(user, data={'password': request.data['new_password'], 'email': user.email, 'username': user.username},
                                    partial=partial, context=dict(request=request))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(data={'detail': 'Password changed'}, status=status.HTTP_200_OK)
