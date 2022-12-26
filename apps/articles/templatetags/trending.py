from django import template
from apps.articles.models import Article

register = template.Library()


@register.inclusion_tag('articles/trending/treanding.html')
def render_trending_news():
    trending_news = Article.objects.filter(trending_article=True)
    return {'trending_news': trending_news}
