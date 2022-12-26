from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class ArticleQuerySet(models.query.QuerySet):

    def published_news(self):
        return self.filter(status=self.model.PUBLISHED)


class ArticleManager(models.Manager):

    def get_query_set(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published_news(self):
        return self.get_query_set().published_news()
