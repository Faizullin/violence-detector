from django.contrib.auth import get_user_model
from .models import Blog

from utils.admin import BaseAdmin, admin



@admin.register(Blog)
class BlogAdmin(BaseAdmin):
    list_display = ("id", 'title', 'description',)
    search_fields = ['title', ]
    raw_id_fields = ('author',)
