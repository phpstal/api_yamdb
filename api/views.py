from rest_framework import viewsets, filters, mixins, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from django_filters import rest_framework, CharFilter, FilterSet


from .models import YamdbUser, Genre, Category, Title
from .serializers import (YamdbUserSerializer, 
                          GenreSerializer, 
                          CategorySerializer, 
                          TitleSerializer)


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


class GenreViewSet(mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
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
    permission_classes = [IsAdminUser]
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter
