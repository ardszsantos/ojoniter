from django.contrib import admin
from django.urls import include, path

from posts.views import feed

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", feed, name="feed"),
    path("accounts/", include("accounts.urls")),
    path("posts/", include("posts.urls")),
]
