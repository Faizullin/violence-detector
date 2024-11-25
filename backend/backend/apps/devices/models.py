from django.contrib.auth import get_user_model
from django.db import models

from apps.file_system.models import File
from utils.models import AbstractTimestampedModel

UserModel = get_user_model()


class Device(AbstractTimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    last_active = models.DateTimeField(verbose_name="Последняя активность" , null=True, blank=True)
    news_create_allowed = models.BooleanField(default=False)


class DeviceConnectionAppBuild(AbstractTimestampedModel):
    version = models.CharField(max_length=210)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)