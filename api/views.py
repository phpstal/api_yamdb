import hashlib
from django.conf import settings
from django.db.models import Avg
from rest_framework import viewsets, filters, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django_filters import rest_framework, CharFilter, FilterSet

from .permissions import IsAdmin, IsAuthor, IsModerator, IsReadOnly
from .models import YamdbUser, Genre, Category, Title, Review
from .serializers import (YamdbUserSerializer,
                          GenreSerializer,
                          CategorySerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          ConfirmationCodeSerializer)


class YamdbUserViewSet(viewsets.ModelViewSet):
    queryset = YamdbUser.objects.all()
    serializer_class = YamdbUserSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ('email',)


class YamdbUserMeViewSet(YamdbUserViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        id = self.request.user.pk
        obj = get_object_or_404(YamdbUser, id=id)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def update(self, request):
        user = self.request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class YamdbUsernameViewSet(YamdbUserViewSet):
    permission_classes = (IsAdmin,)

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        obj = get_object_or_404(YamdbUser, username=username)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def update(self, request, username):
        user = get_object_or_404(YamdbUser, username=username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, username):
        user = get_object_or_404(YamdbUser, username=username)
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin | IsReadOnly,)
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
    permission_classes = (IsAdmin | IsReadOnly,)
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
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin | IsReadOnly,)
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс взаимодействия с моделью Review. """
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnly | IsAdmin | IsModerator | IsAuthor,)

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
    permission_classes = (IsReadOnly | IsAdmin | IsModerator | IsAuthor,)

    def perform_create(self, serializer):
        """Сохранение комментария в бд. """
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        """Получение списка комментариев к отзыву. """
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()


class Registration(APIView):
    permission_classes = (AllowAny,)

    def ConfirmationCodeGenerate(self, email):
        confirmation_code = hashlib.md5(
            f'{email}{settings.SECRET_KEY}'.encode('utf-8')
        ).hexdigest()
        return confirmation_code


class GetConfirmationCode(Registration):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            serializer.save(is_active=False, username=email)
            confirmation_code = self.ConfirmationCodeGenerate(email)
            return Response(
                f'Код подтверждения {confirmation_code} для {email}',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(Registration):
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    def post(self, request):
        email = request.data['email']
        confirmation_code = request.data['confirmation_code']
        confirmation_code_check = self.ConfirmationCodeGenerate(email)
        if confirmation_code == confirmation_code_check:
            user = get_object_or_404(YamdbUser, email=email)
            token = self.get_tokens_for_user(user)
            user.is_active = True
            user.save()
            return Response(token, status=status.HTTP_200_OK)
        return Response(
            'Ошибка в коде или email. Получите новый код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )
