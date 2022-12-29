from django.urls import path
from . import views

urlpatterns = [
    path('rss-feed/', views.ReeFeedView.as_view(), name='rss-feed')
]