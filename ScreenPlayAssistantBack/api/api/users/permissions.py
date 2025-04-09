from rest_framework import permissions
from api.users.roles import UserRoles

class IsValidUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active


class IsRolePermission(IsValidUserPermission):
    role = None
    actions = None

    def has_permission(self, request, view):
        is_role = request.user.is_authenticated and request.user.role == self.role and IsValidUserPermission.has_permission(self, request, view)
        if not is_role:
            return False
        if self.actions is None:
            return True
        return view.action in self.actions
    
    def has_object_permission(self, request, view, obj):
        is_role = request.user.is_authenticated and request.user.role == self.role and IsValidUserPermission.has_permission(self, request, view)
        if not is_role:
            return False
        if self.actions is None:
            return True
        return request.action in self.actions


class IsAdminPermission(IsRolePermission):
    role = UserRoles.ADMIN


class IsSupportPermission(IsRolePermission):
    role = UserRoles.SUPPORT


class IsSupportReadOnlyPermission(IsRolePermission):
    role = UserRoles.SUPPORT
    actions = ['retrieve', 'list']


class AllowAnyCreatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return view.action == 'create'

        if not IsValidUserPermission.has_permission(self, request, view):
            return False
        
        if IsAdminPermission.has_permission(self, request, view):
            return True
        
        if view.action == 'create':
            return False
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        
        if not IsAdminPermission.has_object_permission(self, request, view, obj):
            return False

        if view.action in ['list', 'retrieve']:
            return obj.get_owner() == request.user or obj.is_public()
        elif view.action in ['update', 'partial_update']:
            return obj.get_owner() == request.user
        elif view.action in ['destroy', 'create']:
            return False
        else:
            return False


class CanCrudPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not IsValidUserPermission.has_permission(self, request, view):
            return False
        is_detail_request = 'pk' in request.parser_context['kwargs']
        if view.action == 'create' or is_detail_request:
            # validate if has access to relations
            for fields in view.model._meta.get_fields():
                if fields.name not in request.data:
                    continue
                if fields.is_relation:
                    if not fields.related_model.raw_can_modify(request.user, request.data[fields.name]):
                        print('PERMISSION ERROR: can not link to field', fields.name)
                        return False
        return True
                                                                                                
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if view.action in ['retrieve']:
            return obj.can_modify(request.user, []) or obj.can_read(request.user) or obj.is_public()
        elif view.action in ['update', 'partial_update', 'destroy']:
            return obj.can_modify(request.user, request.data.keys())
        return obj.can_modify(request.user, request.data.keys())
