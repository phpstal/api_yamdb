from rest_framework import permissions

from users.models import Role


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated 
        elif request.method in ('PUT', 'PATCH', 'DELETE'):
            return (request.user.role in {Role.MODERATOR, Role.ADMIN} or 
                    obj.author == request.user or 
                    request.user.is_staff)