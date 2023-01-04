from django.urls import path
from . import views
from apps.general.feed import LatestEntriesFeed

urlpatterns = [
    path('rss-feed/', views.ReeFeedView.as_view(), name='rss-feed'),
    path('latest/feed/', LatestEntriesFeed())
]