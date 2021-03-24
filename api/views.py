from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser


from .models import YamdbUser
from .serializers import YamdbUserSerializer


class YamdbUserViewSet(viewsets.ModelViewSet):
    queryset = YamdbUser.objects.all()
    serializer_class = YamdbUserSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['email']


class YamdbUsernameViewSet(YamdbUserViewSet):
    def get_queryset(self):
        username = self.kwargs['username']
        return YamdbUser.objects.filter(username=username)

    def perform_update(self, serializer):
        username = self.kwargs['username']
        user = get_object_or_404(YamdbUser, username=username)
        serializer.save(user=user)
