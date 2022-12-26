from apps.articles.models import Page
from apps.articles.core import PageBase
from apps.articles.utils import get_object_or_none
from apps.articles.models import Article


class HomePage(PageBase):


    def get_page(self):
        page = get_object_or_none(Page, page_type=Page.HOME_PAGE)
        if not page:
            page = Page.objects.filter(name='Home Page', page_type=Page.HOME_PAGE, status=Page.PUBLISHED)
        page_context = self.get_context()
        return page, page_context, self.render_html(page, page_context)

    @classmethod
    def create_page(cls, **kwargs):
        """
        When new page is created and the status of the page
        is published, old page is set to Inactive.
        """

        new_page = super(HomePage, cls).create_page(**kwargs)
        if new_page.status == new_page.PUBLISHED:
            from_page = kwargs.get('from_page')
            from_page.status = from_page.INACTIVE
            from_page.save()
        return new_page

    def get_context(self):
        context = super().get_context()
        context['lead_news'] = Article.objects.filter(article_type=Article.DEFAULT)
        return context

