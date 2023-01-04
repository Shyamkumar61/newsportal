from django.shortcuts import get_object_or_404
from apps.articles.models import Page
from apps.articles.core import PageBase
from apps.articles.utils import get_object_or_none
from apps.articles.models import Article, ArticleCategory


class CategoryPage(PageBase):

    def get_page(self):
        page = get_object_or_none(Page, page_type=Page.CATEGORY_PAGE)
        if not Page:
            page = Page.objects.filter(name='Category Page', page_type=Page.CATEGORY_PAGE, status=Page.PUBLISHED)
        page_context = self.get_context()
        return page, page_context, self.render_html(page, page_context)

    def get_context(self):
        context = super().get_context()
        category_slug = self.url_path_list[-1]
        category = get_object_or_404(ArticleCategory.objects.only('name', 'name_en', 'slug'), slug=category_slug)
        context['category'] = category
        context['article_list'] = Article.objects.filter(category=category, article_type=Article.DEFAULT, feature_article=False).order_by('-created')
        return context
