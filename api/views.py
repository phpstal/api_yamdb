from rest_framework import viewsets, filters, mixins, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters import rest_framework, CharFilter, FilterSet
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdmin, IsModerator, IsOwner
from .models import YamdbUser, Genre, Category, Title, Review, Comment
from .serializers import (YamdbUserSerializer, 
                          GenreSerializer, 
                          CategorySerializer, 
                          TitleSerializer,
                          ReviewSerializer, 
                          CommentSerializer)


class YamdbUserViewSet(viewsets.ModelViewSet):
    queryset = YamdbUser.objects.all()
    serializer_class = YamdbUserSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['email']
    pagination_class = PageNumberPagination


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
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс взаимодействия с моделью Review. """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner, IsAdmin, IsModerator)
    def get_queryset(self):
        """Получение списка отзывов. """
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Сохранение отзыва в бд. """
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes =(IsAuthenticatedOrReadOnly, IsOwner, IsAdmin, IsModerator)

    def get_queryset(self):
        """Получение списка комментариев к отзыву. """
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохранение комментария в бд. """
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)