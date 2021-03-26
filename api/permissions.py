
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, 
                                        BasePermission,
                                        SAFE_METHODS)

#from users.models import Role


class IsAuthenticatedAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

from rest_framework import permissions, status


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAuthenticatedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            status.HTTP_401_UNAUTHORIZED 
        )


#class IsAuthorOrAdminOrModerator(BasePermission):
#    def has_object_permission(self, request, view, obj):
#        if request.method in SAFE_METHODS:
#            return True
#        elif request.method == 'POST':
#            return request.user.is_authenticated 
#        elif request.method in ('PUT', 'PATCH', 'DELETE'):
#            return (request.user.role in {Role.MODERATOR, Role.ADMIN} or 
#                    obj.author == request.user or 
#                    request.user.is_staff)
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import YamdbUser


class IsActiveUserPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user
                and request.user.is_authenticated
                and request.user.is_active)


class IsOwner(IsActiveUserPermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(IsActiveUserPermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.role == YamdbUser.role.ADMIN


class IsModerator(IsActiveUserPermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff
                or request.user.role == YamdbUser.role.MODERATOR)

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['POST', 'PATCH', 'DELETE']:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_staff
            or request.user.is_superuser
        )