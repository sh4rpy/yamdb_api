from .serializers import *
from .models import *
from .utils import ObjectMixin
from rest_framework import viewsets


class ReviewViewSet(ObjectMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    model = Review
    serializer = ReviewSerializer


class CommentViewSet(ObjectMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    model = Comment
    serializer = CommentSerializer
