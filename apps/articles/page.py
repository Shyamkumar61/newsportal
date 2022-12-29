from .models import Page as PageModel
from apps.articles.pages.home import HomePage
from apps.articles.pages.details import DetailPage
from apps.articles.pages.category import CategoryPage
from apps.articles.pages.video import VideoPage
from apps.articles.pages.tag import TagPage


class PageRendered:

    IDPAGE = 'id-page'

    page_type_class_mapping = {
        PageModel.HOME_PAGE: HomePage,
        PageModel.DETAIL_PAGE: DetailPage,
        PageModel.CATEGORY_PAGE: CategoryPage,
        PageModel.VIDEO_PAGE: VideoPage,
        PageModel.TAG_PAGE: TagPage
    }

    def __init__(self, page_type, url_path_list, request):

        self.url_path_list = url_path_list
        self.page_type = page_type
        self.request = request

    def get_page_and_content(self):
        page_class = self.page_type_class_mapping.get(self.page_type)
        page_instance = page_class(self.url_path_list, self.request)
        return page_instance
