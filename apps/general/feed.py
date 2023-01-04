from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from apps.articles.models import Article


class LatestEntriesFeed(Feed):

    title = "Test"
    link = reverse_lazy('rss-feed')
    description = "Updates on changes and additions to police beat central."

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()