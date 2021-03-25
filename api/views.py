from rest_framework import viewsets, filters, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer


class GenreViewSet(mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED, headers=headers)


class CategoryViewSet(mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    