from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from titles.models import Title
from users.models import User


class Review(models.Model):
    score = models.SmallIntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(10)], verbose_name=_("Оценка"))
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='title_vote', verbose_name=_("Пользователь"))
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='votes', verbose_name=_("Произведение"))
    pub_date = models.DateTimeField(
        auto_now=True, verbose_name=_("Дата оценки"))
    text = models.TextField(verbose_name=_("Текст"))

    def __str__(self):
        return self.title.name


class Comment(models.Model):
    text = models.TextField(verbose_name=_("Текст"))
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_author")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="vote_comment")
