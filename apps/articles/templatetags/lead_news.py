from apps.articles.models import LeadNews, Article
from django import template

register = template.Library()


@register.inclusion_tag('articles/lead/lead_news.html')
def render_lead_news():

    lead_news = list(LeadNews.objects.select_related('article').only('article__title', 'article__cover_image',
                                                                     'article__slug', 'article__created',
                                                                     'article__short_description').order_by('position')[:6])

    if lead_news:
        first_lead = [lead_news[0]]
        second_lead = [lead_news[1]]
        third_lead = lead_news[2:4]


    return {
        'first_lead': first_lead,
        'second_lead': second_lead,
        'third_lead': third_lead,
    }
