from django.contrib import admin
from django.utils.translation import gettext_lazy

from utils.admin import BaseAdmin
from .models import Notification


def mark_read(modeladmin, request, queryset):
    queryset.update(unread=False)


def mark_unread(modeladmin, request, queryset):
    queryset.update(unread=True)


mark_read.short_description = gettext_lazy('Mark selected notifications as read')
mark_unread.short_description = gettext_lazy('Mark selected notifications as unread')


@admin.register(Notification)
class NotificationAdmin(BaseAdmin):
    raw_id_fields = ('recipient',)
    readonly_fields = ('action_object_url', 'actor_object_url', 'target_object_url',)
    list_display = ('recipient', 'actor',
                    'level', 'target', 'unread', 'public')
    list_filter = ('level', 'unread', 'public', 'timestamp', 'recipient')
    actions = [mark_read, mark_unread]

    # def get_queryset(self, request, *args, **kwargs):
    #     qs = super(NotificationAdmin, self).get_queryset(request, *args, **kwargs)
    #     return qs.prefetch_related('actor', '')

    def get_fieldsets_dict(self, request, obj=None):
        default_fieldsets_dict = super().get_fieldsets_dict(request, obj)
        edit_only_fields = ['action_object_url', 'actor_object_url', 'target_object_url', 'timestamp']
        if not obj:
            field_list = default_fieldsets_dict[self.lookup_general_key]["value"]['fields']
            for j in edit_only_fields:
                field_list.remove(j)
            default_fieldsets_dict[self.lookup_general_key]["value"]['fields'] = field_list
            return default_fieldsets_dict
        else:
            default_fieldsets_dict[self.lookup_important_dated_key]["value"]["fields"] = ['timestamp']
            return default_fieldsets_dict
