from django.contrib import admin

from utils.admin import BaseAdmin
from .models import *


# Register your models here.
@admin.register(UserChat)
class UserChatAdmin(BaseAdmin):
    list_filter = ("read_status", "created_at", "updated_at")
    list_display = ("id", "read_status", "created_by", "created_for", "created_at", "updated_at")
    search_fields = ("id", "read_status", "created_by", "created_for", "created_at", "updated_at")
    readonly_fields = ("id",)

    show_full_result_count = False


@admin.register(UserChatMessage)
class UserChatMessageAdmin(BaseAdmin):
    list_filter = ("created_at", "updated_at")
    list_display = ("id", "chat", "created_by", "created_at", "updated_at")
    search_fields = ("id", "chat", "created_at", "created_at", "updated_at")
    readonly_fields = ("id",)

    show_full_result_count = False
