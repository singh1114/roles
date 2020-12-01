from django.contrib.auth.models import User
from django.db import models

from tweets.choices import get_tweet_status_choices
from tweets.constants import TweetStatusConstants


class Tweet(models.Model):
    # No images as of now.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(
        choices=get_tweet_status_choices(),
        default=TweetStatusConstants.APPROVED.value
    )
    updated_text = models.TextField(max_length=200)
