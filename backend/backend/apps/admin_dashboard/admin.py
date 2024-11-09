from django.apps import apps
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django_softdelete.models import SoftDeleteModel


class CustomAdminSite(admin.AdminSite):
    def get_urls(
            self,
    ):
        default_urls = super().get_urls()
        return [
            path(
                "trash/list/",
                self.admin_view(self.trashed_items_view),
                name="custom_page",
            ),
        ] + default_urls

    def trash_list_page(self, request):
        context = {
            "text": "Hello Admin",
            "page_name": "Custom Page",
            "app_list": self.get_app_list(request),
            **self.each_context(request),
        }
        return TemplateResponse(request, "admin/soft_deleted_items/list.html", context)

    def trashed_items_view(self, request):
        models = apps.get_models()
        soft_deleted_items = []
        search_query = request.GET.get('search', '')
        sort_field = request.GET.get('sort', 'deleted_at')

        for model in models:
            if issubclass(model, SoftDeleteModel):
                queryset = model.all_objects.filter(is_deleted=True)
                if search_query:
                    queryset = queryset.filter(
                        name__icontains=search_query)  # Adjust this filter as per your model fields
                soft_deleted_items.extend(queryset)

        # Sorting
        reverse = sort_field.startswith('-')
        sort_field = sort_field.lstrip('-')
        soft_deleted_items.sort(key=lambda x: getattr(x, sort_field, None) or x.id, reverse=reverse)

        context = dict(
            self.each_context(request),
            title="Trashed Items",
            soft_deleted_items=soft_deleted_items,
        )
        return TemplateResponse(request, "admin/soft_deleted_items/list.html", context)
