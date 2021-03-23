from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Genre
from .serializers import GenreSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #pagination_class = PageNumberPagination
    #permission_classes = PERMISSION_CLASSES
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    #def perform_create(self, serializer, *args, **kwargs):
    #    serializer.save(author=self.request.user)