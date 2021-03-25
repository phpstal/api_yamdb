from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
