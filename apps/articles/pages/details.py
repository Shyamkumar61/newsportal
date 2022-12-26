from django.shortcuts import get_object_or_404

from apps.articles.models import Page
from apps.articles.core import PageBase
from apps.articles.utils import get_object_or_none
from apps.articles.models import Article


class DetailPage(PageBase):

    def get_page(self):
        page = get_object_or_none(Page, page_type=Page.DETAIL_PAGE)
        if not page:
            page = page.objects.filter(name='Detail Page', page_type=Page.DETAIL_PAGE, status=Page.PUBLISHED)
        page_context = self.get_context()
        return page, page_context, self.render_html(page, page_context)

    def get_context(self):
        context = super().get_context()
        article_slug = self.url_path_list[-1]
        context['article'] = get_object_or_404(Article.objects.select_related('category'), slug=article_slug, status=Article.PUBLISHED)
        return context
