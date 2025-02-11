from django.contrib.auth import get_user_model

from apps.devices.models import Device, AbstractLocationModel
from apps.file_system.models import File
from utils.models import AbstractTimestampedModel, models

UserModel = get_user_model()


class PredictionAttempt(AbstractTimestampedModel,AbstractLocationModel):
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    device_name = models.CharField(max_length=255)
    image = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)


class Prediction(AbstractTimestampedModel):
    type = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    attempt = models.ForeignKey(PredictionAttempt, on_delete=models.SET_NULL, null=True)
    result = models.TextField()  # AI prediction result in json format
    confidence = models.FloatField()  # Confidence score
    message = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)


class News(AbstractTimestampedModel):
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    prediction_attempt = models.ForeignKey(PredictionAttempt, on_delete=models.SET_NULL, null=True)
    data = models.TextField(null=True, blank=True)
