from django.shortcuts import render
from django.views.generic import TemplateView
from apps.articles.models import ArticleCategory

# Create your views here.


class ReeFeedView(TemplateView):
    
    template_name = 'general/rss_feed.html'
    
    def get_context_data(self, **kwargs):
        context = super(ReeFeedView, self).get_context_data(**kwargs)
        categories = ArticleCategory.objects.filter(depth=1)
        context['categories'] = categories
        return context




    
