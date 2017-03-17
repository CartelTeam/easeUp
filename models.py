from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class tweet(models.Model):
    tweets = models.CharField(max_length=1000)
    user_name=models.CharField(max_length=200)

    def __str__(self):
        return self.tweets


class Profile(models.Model):
    user = models.ForeignKey(User)
    user_name = models.CharField(max_length=200)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user_name)


