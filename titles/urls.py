from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('', include(router.urls)),
]
