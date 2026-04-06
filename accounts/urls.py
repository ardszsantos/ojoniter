from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit_profile, name="edit_profile"),
    path("<str:username>/", views.profile, name="profile"),
    path("<str:username>/follow/", views.follow_toggle, name="follow_toggle"),
    path("<str:username>/followers/", views.followers_list, name="followers_list"),
    path("<str:username>/following/", views.following_list, name="following_list"),
]
