from django.contrib import admin

from apps.contact_us.models import ContactDetail
from utils.admin import BaseAdmin


@admin.register(ContactDetail)
class ContactDetailAdmin(BaseAdmin):
    list_display = ('subject', 'name', 'email', 'phone',)
