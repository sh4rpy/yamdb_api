from django.db import models
from django.utils.translation import ugettext_lazy as _


class Title(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    year = models.IntegerField(null=True, blank=True, verbose_name='Дата')
    description = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Описание')
    genre = models.ManyToManyField('Genre', related_name='title', blank=True,)
    category = models.ForeignKey(
        'Category', related_name='title', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(
        default=None, null=True, blank=True, verbose_name='Рейтинг')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name
