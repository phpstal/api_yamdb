from rest_framework import viewsets, filters, mixins, serializers
from django_filters import rest_framework, CharFilter, FilterSet

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


class CategoryViewSet(mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', 
                       lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', 
                          lookup_expr='icontains')
    name = CharFilter(field_name='name', 
                      lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = []
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter
