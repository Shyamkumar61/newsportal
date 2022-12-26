from django.urls import path, re_path
from . import views

urlpatterns = [
    path('search/', views.Search.as_view(), name='search'),
    path('videos/', views.Videos.as_view(), name='videos'),
    re_path(r'^(?P<path>.*)$', views.ArticleController.as_view(), name='articles-controller'),
]
