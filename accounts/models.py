from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    display_name = models.CharField(max_length=50, blank=True)
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)

    def get_display_name(self):
        return self.display_name or self.username

    def get_initial(self):
        return (self.display_name or self.username)[0].upper()

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()
