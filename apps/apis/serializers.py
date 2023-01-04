from rest_framework import serializers
from apps.articles.models import Article, ArticleCategory
from django.conf import settings

web = 'http://localhost:8000'


class Articles(serializers.ModelSerializer):

    cover_image = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        field = (
            'title', 'description', 'cover_image', 'absolute_url'
        )

    def get_cover_image(self, obj):
        if obj.cover_image:
            return settings.MEDIA_URL + obj.cover_image
        else:
            return ''

    def get_absolute_url(self, obj):
        if obj.absolute_url:
            return web + "/news/%s/%s" % (obj.category.name_en, obj.slug)
        else:
            return web + "/news/%s/" % (obj.slug)
