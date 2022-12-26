from apps.articles.core import PageBase
from apps.articles.models import Article
from apps.articles.utils import get_object_or_none
from apps.articles.models import Page


class VideoPage(PageBase):
    
    def get_context(self):
        context = super(VideoPage, self).get_context()
        video_ids = list()
        context['videos'] = Article.objects.filter(type=Article.YOUTUBE)
        return context

    def get_page(self):
        page = get_object_or_none(Page, page_type=Page.VIDEO_PAGE)
        if not page:
            page = Page.objects.filter(name='Video Page', page_type=Page.VIDEO_PAGE, status=Page.PUBLISHED)
        page_context = self.get_context()
        return page, page_context, self.render_html(page, page_context)
