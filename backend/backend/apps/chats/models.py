from django.contrib.auth import get_user_model
from django.db import models
from django_softdelete.models import SoftDeleteModel

from utils.models import AbstractTimestampedModel

UserModel = get_user_model()


class UserChat(AbstractTimestampedModel, SoftDeleteModel):
    read_status = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        UserModel, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name='sender')
    created_for = models.ForeignKey(
        UserModel, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name='receiver')

    class Meta:
        verbose_name_plural = "User Chat Rooms"

    def __str__(self):
        return str(self.id)


class UserChatMessage(AbstractTimestampedModel):
    message = models.CharField(max_length=500, null=True, blank=True)
    chat = models.ForeignKey(UserChat, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(
        UserModel, blank=True, null=True, default=None, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "User Chat Messages"

    def __str__(self):
        return self.message
