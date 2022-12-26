from django import template
from apps.articles.models import Article

register = template.Library()

@register.inclusion_tag("articles/feature_news/feature_articles.html")
def render_feature_news(category):
    category_news = Article.objects.filter(category=category, feature_article=True).order_by('-created')[:8]
    if category_news:
        first_lead = [category_news[0]]
        second_lead = category_news[1:3]
        third_lead = category_news[4:6]

    return {
        'first_lead': first_lead,
        'second_lead': second_lead,
        'third_lead': third_lead,
    }
