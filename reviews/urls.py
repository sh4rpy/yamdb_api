from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(
    '(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')
router.register('', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
