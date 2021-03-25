from django.urls import path, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,)

from .views import GenreViewSet, CategoryViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('users', TitleViewSet)

API_V = 'v1/'

urlpatterns = [
    path(API_V, include(router_v1.urls)),
    path(API_V + 'token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(API_V + 'token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
