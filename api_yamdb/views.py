from rest_framework import viewsets
from .models import Genre
from .serializers import GenreSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = PERMISSION_CLASSES
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['group']

    #def perform_create(self, serializer, *args, **kwargs):
    #    serializer.save(author=self.request.user)