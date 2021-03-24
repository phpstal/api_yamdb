from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import YamdbUsernameViewSet, YamdbUserViewSet

router = DefaultRouter()
router.register('users', YamdbUserViewSet, basename='users')

auth_urls = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email/', TokenRefreshView.as_view(), name='token_refresh')
]

YamdbUsernameMethods = {
    'get': 'list',
    'patch': 'update',
    'del': 'destroy'
}

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path(
        'v1/users/<str:username>/',
        YamdbUsernameViewSet.as_view(YamdbUsernameMethods),
        name='user'
    ),
    path('v1/', include(router.urls)),
]
