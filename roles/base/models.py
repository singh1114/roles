from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.constants import LogTypeConstants, LogActionConstants

from base.choices import get_log_type_choices, get_log_action_choices


class ActionLogModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    log_type = models.IntegerField(
        choices=get_log_type_choices(),
        default=LogTypeConstants.ACTION
    )
    action = models.IntegerField(
        choices=get_log_action_choices(),
        default=LogActionConstants.TWEET
    )
    content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                     on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
