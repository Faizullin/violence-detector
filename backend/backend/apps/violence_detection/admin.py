from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Prediction, PredictionAttempt, News


@admin.register(PredictionAttempt)
class PredictionAttemptAdmin(BaseAdmin):
    list_display = ("id", 'device_name', 'device',)
    search_fields = ['device_name', ]
    raw_id_fields = ('device', "image",)


@admin.register(Prediction)
class PredictionAdmin(BaseAdmin):
    list_display = ("id", "type", "attempt")
    search_fields = ['type', ]
    raw_id_fields = ('device', "attempt",)


@admin.register(News)
class PredictionAdmin(BaseAdmin):
    list_display = ("id", "title", "prediction_attempt", "author")
    search_fields = ['title', ]
    raw_id_fields = ('prediction_attempt', "author",)
