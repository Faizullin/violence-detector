from django.contrib import admin
from .models import File
from utils.admin import BaseAdmin, admin

# Register your models here.
@admin.register(File)
class FileAdmin(BaseAdmin):
    list_display = ('id', 'file', "name")
    search_fields = ['name', ]
