from django import template
from apps.articles.models import Article, ArticleCategory


register = template.Library()


@register.inclusion_tag('articles/breadcrumb/detail_breadcrumb.html')
def render_breadcrumb(article):
    if isinstance(article, Article):
        category = article.category
        if category:
            parent = category.get_parent()
            return {'category': category, 'parent': parent, 'article': article}
        else:
            return {'article': article}
    return {}

@register.inclusion_tag('articles/breadcrumb/category-level-one.html')
def category_level_one(category):
    return {'category': category}

def render_breadcrumb_cat_two(category):
    """
    function that renders a component to html if one exist
    if a template_name is passed that one has higher priority.
    """
    if isinstance(category, ArticleCategory):
        parent = category.get_parent()
        return {'category':category,'parent':parent}
    else:
        return {}

def render_breadcrumb_cat_two_listing(category):
    """
    function that renders a component to html if one exist
    if a template_name is passed that one has higher priority.
    """
    if isinstance(category, ArticleCategory):
        more = 'ALL'
        parent = category.get_parent()
        return {'category':category,'parent':parent}
    else:
        return {} 


@register.inclusion_tag('articles/breadcrumb/video_page.html')
def render_breadcrumb_video():
    """
    function that renders a component to html if one exist
    if a template_name is passed that one has higher priority.
    """
    return {}


@register.inclusion_tag('articles/breadcrumb/search_page.html')
def render_search():
    """
    function that renders a component to html if one exist
    if a template_name is passed that one has higher priority.
    """
    return {}
