from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status
from .models import *


class ObjectMixin():
    model = None
    serializer = None

    def list(self, request, title_id=None, review_id=None):
        if review_id:
            obj = self.model.objects.filter(review=review_id)
        elif title_id:
            obj = self.model.objects.filter(title__id=title_id)
        else:
            obj = self.model.objects.all()
        page = self.paginate_queryset(obj)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer(obj, many=True)
        return Response(serializer.data)

    def create(self, request, title_id=None, review_id=None):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            if review_id:
                review = get_object_or_404(Review, id=review_id)
                serializer.save(author=request.user, review=review)
            elif title_id:
                title = get_object_or_404(Title, id=title_id)
                reviews_author_list = Review.objects.filter(
                    title=title).values_list('author__email', flat=True)
                if request.user.email in list(reviews_author_list):
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save(author=request.user, title=title)
                rat = Review.objects.filter(
                    title=title).aggregate(Avg('score'))['score__avg']
                rat = round(rat, 0)
                title.rating = rat
                title.save()
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, title_id=None, review_id=None, pk=None):
        if title_id:
            obj = get_object_or_404(self.model, pk=pk)
        else:
            obj = request.user if pk == 'me' else get_object_or_404(
                self.model, username=pk)
        serializer = self.serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, title_id=None, review_id=None, pk=None):
        if pk == 'me':
            obj = request.user
        else:
            obj = get_object_or_404(self.model, pk=pk) if title_id else get_object_or_404(
                self.model, username=pk)
        if title_id and obj.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if title_id:
                title = get_object_or_404(Title, id=title_id)
                rat = Review.objects.filter(
                    title=title).aggregate(Avg('score'))['score__avg']
                rat = round(rat, 0)
                title.rating = rat
                title.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, title_id=None, review_id=None, pk=None):
        if pk == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            obj = get_object_or_404(self.model, pk=pk) if title_id else get_object_or_404(
                self.model, username=pk)
        if title_id and obj.author != request.user and request.user.role == 'user':
            return Response(status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
