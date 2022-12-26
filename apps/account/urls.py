from django.urls import path, re_path
from . import views

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('singup/', views.SingupView.as_view(), name='singup'),

]
