from apps.articles.core import PageBase
from apps.articles.models import Article
from apps.articles.utils import get_object_or_none
from apps.articles.models import Page


class TagPage(PageBase):

    def get_context(self):
        context = super(TagPage, self).get_context()
        tag = self.url_path_list[-1]
        context['tag_list'] = Article.objects.filter(tags__slug=tag)
        return context

    def get_page(self):
        page = get_object_or_none(Page, page_type=Page.TAG_PAGE)
        if not page:
            page = page.objects.filter(name='Tag Page', page_type=Page.TAG_PAGE, status=Page.PUBLISHED)
        page_context = self.get_context()
        return page, page_context, self.render_html(page, page_context)
