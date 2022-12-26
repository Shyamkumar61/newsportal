from django.views.generic import TemplateView
from .controller import PageController
from apps.articles.models import Article
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

# Create your views here.


class Search(TemplateView):

    template_name = 'articles/search.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        if search:
            search = search.strip()
            articles = Article.objects.published_news().filter(
                Q(title__icontains=search) | Q(tags__name__icontains=search) |
                Q(category__name__icontains=search)
            )
            context['articles'] = articles
        else:
            context['articles'] = Article.objects.none()
        context['search'] = search
        return context


class ArticleController(TemplateView):
    """
    This view handles

    1.Home Page.
    2.Article Listing
    3.Article Detail Page
    4.Search Page
    """
    template_name = 'articles/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        controller = PageController(kwargs.get('path'), self.request.GET, self.request)
        page, page_context, page_template = controller.get_page_and_template()
        context['page_template'] = page_template
        context['page_context'] = page_context
        context['page'] = page
        return context


class Videos(TemplateView):

    template_name = 'articles/video.html'


class AboutController(TemplateView):

    template_name = 'articles/about.html'




