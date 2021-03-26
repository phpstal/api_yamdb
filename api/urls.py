from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, 
                                            TokenRefreshView)

from .views import (YamdbUsernameViewSet, 
                    YamdbUserViewSet, 
                    YamdbUserMeViewSet,
                    GetToken,
                    GetConfirmationCode,
                    GenreViewSet, 
                    CategoryViewSet, 
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet)


router = DefaultRouter()
router.register('users', YamdbUserViewSet, basename='users')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'^titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

auth_urls = [
    path('token/', GetToken.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email/', GetConfirmationCode.as_view(), name='confirmation_code')
]

YamdbUsernameMethods = {
    'get': 'list',
    'patch': 'update',
    'delete': 'destroy'
}

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path(
        'v1/users/me/',
        YamdbUserMeViewSet.as_view(YamdbUsernameMethods),
        name='my_user'
    ),
    path(
        'v1/users/<str:username>/',
        YamdbUsernameViewSet.as_view(YamdbUsernameMethods),
        name='user'
    ),
    path('v1/', include(router.urls)),
]
