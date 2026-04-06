from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("explore/", views.explore, name="explore"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("<int:pk>/like/", views.like_toggle, name="like_toggle"),
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("<int:pk>/delete/", views.delete_post, name="delete_post"),
]
