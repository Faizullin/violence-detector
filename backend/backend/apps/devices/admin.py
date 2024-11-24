from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Device, DeviceConnectionAppBuild


@admin.register(Device)
class DeviceAdmin(BaseAdmin):
    list_display = ("id", 'name', 'user',)
    search_fields = ['name', ]
    raw_id_fields = ('user',)


@admin.register(DeviceConnectionAppBuild)
class DeviceConnectionAppBuildAdmin(BaseAdmin):
    list_display = ("id", 'version', 'available',)
    raw_id_fields = ('file',)
