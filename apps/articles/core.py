from django.template import Template, Context
from apps.articles.models import Page as PageModel
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import add_domain


class PageBase:

    def __init__(self, url_path_list, request):
        self.url_path_list = url_path_list
        self.request = request

    def get_context(self):
        context = dict()
        return context

    def get_page(self):
        raise NotImplementedError

    def render_html(self, page, page_context=None):
        """
        read the page html from db and render using the render() method.
        """
        context = dict()
        if page_context:
            context['page_context'] = page_context
        else:
            context['page_context'] = dict()
        # adding request object to context
        context['request'] = self.request

        #
        user = self.request.user
        context['user'] = user
        if user.has_perm('articles.can_publish_article'):
            context['can_edit_article'] = True
        else:
            context['can_edit_article'] = False
        is_wellwisher = self.request.user.groups.filter(name__in=['Wellwisher'])
        if is_wellwisher:
            is_wellwisher = True
        else:
            is_wellwisher = False
        context['is_wellwisher'] = is_wellwisher
        tp = Template(page.layout)
        return tp.render(Context(context))

    def render_preview(self, page, page_context=None):
        """
        read the page html from db and render using the render() method.
        """
        context = dict()
        if page_context:
            context['page_context'] = page_context
        context['request'] = self.request
        tp = Template(page.layout)
        return tp.render(Context(context))

    @classmethod
    def create_page(cls, from_page, layout, page_type, new_page_status,
                    published_date, edit_mode, preview, page_linked_contents=None):
        if edit_mode == PageModel.EDIT:
            # when the mode is edit no need to create a new page object, instead modify
            # the from_page object.
            new_page = from_page
            new_page.layout = layout
            new_page.published_date = published_date
            new_page.status = new_page_status
            new_page.page_type = page_type
        elif edit_mode == PageModel.DUPLICATE:
            # TOD ability to change page type.
            from_page, new_page = cls.create_new_page(from_page, layout, page_type, new_page_status, published_date,
                                                      duplicate=True)
        else:
            # considered as MODIFY.
            from_page, new_page = cls.create_new_page(from_page, layout, page_type, new_page_status, published_date)

        if not preview:
            # save the pages if not preview.
            from_page.save()
            new_page.save()

            # if a default page exist for from_page, link it to the new_page.
            if from_page.default_page.exists() and new_page.status == new_page.PUBLISHED:
                from_page.default_page.all().update(page=new_page)

        return from_page, new_page

    @staticmethod
    def create_new_page(from_page, layout, page_type, new_page_status, published_date, duplicate=False):
        new_page = PageModel()
        new_page.name = from_page.name
        new_page.page_type = from_page.page_type if not duplicate else page_type
        new_page.layout = layout
        new_page.status = new_page_status
        new_page.published_date = published_date

        if not duplicate:
            # deactivate the from page if the status of new page is published.
            if new_page.status == new_page.PUBLISHED:
                from_page.status = from_page.INACTIVE
        return from_page, new_page

    def _build_meta(self, name, content):
        return {"name": name, "content": content}

    def _build_meta_property(self, meta_property, content):
        return {"property": meta_property, "content": content}

    def build_absolute_url(self, url):
        current_site = get_current_site(self.request)
        return add_domain(current_site.domain, url, self.request.is_secure())
