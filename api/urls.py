from django.urls import path, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,)
from .views import GenreViewSet

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet)
#router_v1.register('group', GroupViewSet)
#router_v1.register('follow', FollowViewSet, basename='follow')
#router_v1.register(
#    r'posts/(?P<post_id>\d+)/comments',
#    CommentViewSet,
#    basename='comments'
#)
API_V = 'v1/'

urlpatterns = [
    path(API_V, include(router_v1.urls)),
#    path(API_V + 'token/',
#         TokenObtainPairView.as_view(),
#         name='token_obtain_pair'),
#    path(API_V + 'token/refresh/',
#         TokenRefreshView.as_view(),
#         name='token_refresh'),
]
