import json

from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from apps.file_system.fields import ImageWithThumbsField
from utils.models import AbstractMetaModel


def restore_queryset(modeladmin, request, queryset):
    if isinstance(queryset, QuerySet):
        for obj in queryset:
            obj.restore(strict=False)
    else:
        # queryset.deleted_at = None
        # queryset.is_deleted = False
        queryset.restore()


def soft_delete_queryset(modeladmin, request, queryset):
    if isinstance(queryset, QuerySet):
        for obj in queryset:
            obj.delete()
    else:
        queryset.delete()


def hard_delete_queryset(modeladmin, request, queryset):
    if isinstance(queryset, QuerySet):
        for obj in queryset:
            obj.hard_delete()
    else:
        queryset.hard_delete()


class SoftDeleteFilter(SimpleListFilter):
    title = 'is deleted'
    parameter_name = 'is_deleted'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Deleted Softly'),
            ('false', 'Not Deleted'),
            ('all', 'All'),
        )

    def queryset(self, request, queryset):
        value = {
            'true': False,
            'false': True,
            'all': 'ALL',
        }[self.value() or 'false']
        if value == 'ALL':
            return queryset

        return queryset.filter(deleted_at__isnull=value)


class ImageWithThumbsAdminWidget(forms.ClearableFileInput):
    template_name = 'admin_dashboard/forms/image-with-thumbs-widget.html'

    def __init__(self, *args, **kwargs):
        self.app_name = kwargs.pop('app_name')
        self.model_name = kwargs.pop('model_name')
        self.object_id = kwargs.pop('object_id')
        self.model_field = kwargs.pop('model_field')
        self.field_name = self.model_field.name
        self.field_type = kwargs.pop('field_type')
        self.field_method = kwargs.pop('field_method')
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        file_value = None
        if value:
            file_value = {
                "name": value.name,
                "relative_path": value.name.split('/')[-1],
                "url": self.request.build_absolute_uri(value.url),
                # "size": value.size,
            }
        context.update({
            "obj": {
                'app_name': self.app_name,
                'model_name': self.model_name,
                'object_id': self.object_id,
                'field_name': self.field_name,
                'field_type': self.field_type,
                'field_method': self.field_method,
                'value_json': json.dumps(file_value),
                'value': file_value,
            },
            "available_sizes": self.model_field.sizes,
        })
        print(context)
        return context


class FileAdminField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        app_name = kwargs.pop('app_name')
        model_name = kwargs.pop('model_name')
        object_id = kwargs.pop('object_id')
        field = kwargs.pop('field')
        field_type = kwargs.pop('field_type')
        field_method = kwargs.pop('field_method')
        widget = ImageWithThumbsAdminWidget(
            app_name=app_name,
            model_name=model_name,
            object_id=object_id,
            model_field=field,
            field_type=field_type,
            field_method=field_method,
            request=request,
        )
        super().__init__(widget=widget, *args, **kwargs)


class FileAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            model_field = self._meta.model._meta.get_field(field_name)
            if isinstance(model_field, ImageWithThumbsField):
                self.fields[field_name] = FileAdminField(
                    app_name=self._meta.model._meta.app_label,
                    model_name=self._meta.model.__name__,
                    object_id=kwargs.get('instance').id if kwargs.get('instance') else None,
                    field=model_field,
                    field_type='thumbnail_image',
                    field_method='attach_field',
                    request=request,
                )


class BaseAdmin(admin.ModelAdmin):
    has_default_timestamps = False
    has_soft_delete = False
    has_html_meta = False
    lookup_important_dated_key = "important_dates"
    lookup_general_key = "general"
    lookup_html_meta_key = "html_meta"
    lookup_key_list = [lookup_general_key]

    def __init__(self, model, admin_site):
        super(BaseAdmin, self).__init__(model, admin_site)
        self.has_default_timestamps = self.check_has_default_timestamps()
        self.has_soft_delete = self.check_has_soft_delete()
        self.has_html_meta = self.check_has_html_meta()
        if self.has_default_timestamps:
            self.readonly_fields += ("created_at", "updated_at",)
        if self.has_soft_delete:
            self.readonly_fields += ("deleted_at", "restored_at",)

    # def get_form(self, request, obj=None, **kwargs):
    #     self.form = FileAdminForm
    #     foo_form = super(BaseAdmin, self).get_form(request, obj, **kwargs)
    #
    #     class RequestFooForm(foo_form):
    #         def __new__(cls, *args, **kwargs):
    #             kwargs['request'] = request
    #             return foo_form(*args, **kwargs)
    #
    #     return RequestFooForm

    def get_ordering(self, request):
        if self.has_default_timestamps and self.ordering is None:
            return ['-updated_at']
        return self.ordering

    def get_readonly_fields(self, request, obj=None):
        default = super().get_readonly_fields(request, obj)
        # if self.has_default_timestamps:
        #     default += ('created_at', 'updated_at',)
        return default

    def check_has_default_timestamps(self):
        field_name_list = [field.name for field in self.model._meta.get_fields()]
        return 'created_at' in field_name_list and 'updated_at' in field_name_list

    def check_has_soft_delete(self):
        field_name_list = [field.name for field in self.model._meta.get_fields()]
        return 'deleted_at' in field_name_list and 'restored_at' in field_name_list

    def check_has_html_meta(self):
        return issubclass(self.model, AbstractMetaModel)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_soft_delete'] = self.has_soft_delete
        extra_context['has_default_timestamps'] = self.has_default_timestamps
        return super().changelist_view(request, extra_context=extra_context)

    def get_list_filter(self, request):
        default_list = super().get_list_filter(request)
        if self.has_soft_delete:
            default_list += (SoftDeleteFilter,)
        return default_list

    def get_object(self, request, object_id, from_field=None):
        queryset = self.get_queryset(request, show_all=True)
        model = queryset.model
        field = (
            model._meta.pk if from_field is None else model._meta.get_field(from_field)
        )
        try:
            object_id = field.to_python(object_id)
            return queryset.get(**{field.name: object_id})
        except (model.DoesNotExist, ValidationError, ValueError):
            return None

    def get_queryset(self, request, show_all=False):
        is_deleted_filter = request.GET.get("is_deleted", "0")
        # if is_deleted_filter == "1" and self.has_soft_delete:
        #     qs = self.model.deleted_objects.all()
        # elif show_all and self.has_soft_delete:
        #     qs = self.model.global_objects.all()
        # elif self.has_soft_delete:
        #     qs = self.model.objects.all()
        # else:
        #     qs = self.model.objects.all()
        if self.has_soft_delete:
            if is_deleted_filter == "1" or is_deleted_filter == "true":
                qs = self.model.deleted_objects.all()
            else:
                qs = self.model.global_objects.all()
        else:
            qs = self.model.objects.all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_actions(self, request):
        default = super().get_actions(request)
        if self.has_soft_delete:
            default.update({
                "restore": (restore_queryset, "restore", "Restore selected items"),
                "hard_delete": (hard_delete_queryset, "hard_delete", "Hard delete selected items"),
            })
        return default

    def delete_queryset(self, request, queryset):
        soft_delete_queryset(_, request, queryset)

    def delete_model(self, request, obj):
        soft_delete_queryset(_, request, obj)

    def get_fieldsets(self, request, obj=None):
        fieldsets_dict = self.get_fieldsets_dict(request, obj)
        fieldsets = []
        for key in self.lookup_key_list:
            item = fieldsets_dict[key]
            fieldsets.append((item['label'], item['value']))
        return fieldsets

    def get_fieldsets_dict(self, request, obj=None):
        default_fieldsets = super().get_fieldsets(request, obj)
        new_fieldsets_dict = dict()
        if not self.lookup_general_key in new_fieldsets_dict:
            new_fieldsets_dict[self.lookup_general_key] = {
                "label": default_fieldsets[0][0],
                "value": default_fieldsets[0][1],
            }
        if not self.lookup_important_dated_key in new_fieldsets_dict:
            new_fieldsets_dict[self.lookup_important_dated_key] = {
                "label": _("Important dates"),
                "value": {
                    "fields": [],
                },
            }
        if self.has_html_meta and (self.lookup_html_meta_key not in new_fieldsets_dict):
            new_fieldsets_dict[self.lookup_html_meta_key] = {
                "label": _("Meta"),
                "value": {
                    "fields": [],
                },
            }

        if self.has_default_timestamps:
            if 'created_at' in new_fieldsets_dict[self.lookup_general_key]["value"]["fields"]:
                new_fieldsets_dict[self.lookup_general_key]["value"]["fields"].remove('created_at')
            if 'updated_at' in new_fieldsets_dict[self.lookup_general_key]["value"]["fields"]:
                new_fieldsets_dict[self.lookup_general_key]["value"]["fields"].remove('updated_at')
            new_fieldsets_dict[self.lookup_important_dated_key]["value"]["fields"].append('created_at')
            new_fieldsets_dict[self.lookup_important_dated_key]["value"]["fields"].append('updated_at')
        if self.has_soft_delete:
            if 'deleted_at' in new_fieldsets_dict[self.lookup_general_key]["value"]["fields"]:
                new_fieldsets_dict[self.lookup_general_key]["value"]["fields"].remove('deleted_at')
            if 'restored_at' in new_fieldsets_dict[self.lookup_general_key]["value"]["fields"]:
                new_fieldsets_dict[self.lookup_general_key]["value"]["fields"].remove('restored_at')
            new_fieldsets_dict[self.lookup_important_dated_key]["value"]["fields"].append('deleted_at')
            new_fieldsets_dict[self.lookup_important_dated_key]["value"]["fields"].append('restored_at')

        if self.has_html_meta:
            for key in ['use_ssr', 'render_url', 'meta_title', 'meta_keywords', 'meta_description']:
                new_fieldsets_dict[self.lookup_html_meta_key]["value"]["fields"].append(key)
                if key in new_fieldsets_dict[self.lookup_general_key]["value"]["fields"]:
                    new_fieldsets_dict[self.lookup_general_key]["value"]["fields"].remove(key)

        if obj is None:
            if self.has_default_timestamps or self.has_soft_delete:
                del new_fieldsets_dict[self.lookup_important_dated_key]
            if self.has_html_meta:
                del new_fieldsets_dict[self.lookup_html_meta_key]
        else:
            self.lookup_key_list = [self.lookup_general_key]
            if self.has_html_meta:
                self.lookup_key_list.append(self.lookup_html_meta_key)
            if self.has_default_timestamps or self.has_soft_delete:
                self.lookup_key_list.append(self.lookup_important_dated_key)

        return new_fieldsets_dict