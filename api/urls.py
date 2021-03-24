from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet,
    CommentViewSet
)
from django.urls import path, include


router = DefaultRouter()
router.register(r'titles/(?P<title_id>[0-9]+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>[0-9]+)/reviews/'
                r'(?P<reviews_id>[0-9]+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]