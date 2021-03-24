from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsAuthenticatedAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
