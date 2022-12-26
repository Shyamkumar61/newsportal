from django.http import Http404

from apps.articles.page import PageRendered
from .models import Page


class PageController:
    """
    A controller that handles multiple routes.
    """

    def __init__(self, path, get_param, requets):
        self.kwargs_splitted = path.split('/')
        self.get_param = get_param
        self.kwargs_splitted = list(filter(None, self.kwargs_splitted))
        self.request = requets

    def get_page_and_template(self):
        page_object, page_template, is_edit = None, None, False

        if len(self.kwargs_splitted) == 0:
            page_rendered = PageRendered(Page.HOME_PAGE, self.kwargs_splitted, self.request)
            page = page_rendered.get_page_and_content()
            page_object, page_context, page_template = page.get_page()

        elif self.kwargs_splitted[0] == 'news' and len(self.kwargs_splitted) == 2:
            page_rendered = PageRendered(Page.CATEGORY_PAGE, self.kwargs_splitted, self.request)
            page = page_rendered.get_page_and_content()
            page_object, page_context, page_template = page.get_page()

        elif self.kwargs_splitted[0] == 'section' and len(self.kwargs_splitted) == 2:
            page_rendered = PageRendered(Page.VIDEO_PAGE, self.kwargs_splitted, self.request)
            page = page_rendered.get_page_and_content()
            page_object, page_context, page_template = page.get_page()

        elif self.kwargs_splitted[0] == 'tag' and len(self.kwargs_splitted) == 2:
            page_rendered = PageRendered(Page.TAG_PAGE, self.kwargs_splitted, self.request)
            page = page_rendered.get_page_and_content()
            page_object, page_context, page_template = page.get_page()

        elif self.kwargs_splitted[0] == 'news' and len(self.kwargs_splitted) == 3:
            page_rendered = PageRendered(Page.DETAIL_PAGE, self.kwargs_splitted, self.request)
            page = page_rendered.get_page_and_content()
            page_object, page_context, page_template = page.get_page()
        else:
            raise Http404

        return page_object, page_context, page_template

