from django.urls import path, re_path
from . import views

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('singup/', views.SingupView.as_view(), name='singup'),
    path('profile/', views.ProfileHomeView.as_view(), name="profile"),
    path('edit_profile/', views.EditProfileView.as_view(), name="edit_profile")
]
