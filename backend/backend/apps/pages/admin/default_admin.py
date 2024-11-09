from apps.pages.models import PageDocument, PageStyle
from utils.admin import BaseAdmin, admin


@admin.register(PageStyle)
class SiteDocumentAdmin(BaseAdmin):
    list_display = ('title',)
    search_fields = ['title']


@admin.register(PageDocument)
class SiteDocumentAdmin(BaseAdmin):
    # add_form_template = 'admin/blogs/sitedocument/change_form.html'
    # change_form_template = 'admin/blogs/sitedocument/change_form.html'
    # readonly_fields = ('preview_url',)
    list_display = ('title',)
    search_fields = ['title']

    # def preview_url(self, obj):
    #     # print("preview_url")
    #     link = reverse_lazy('blogs:site-document-retrieve-api', kwargs={"pk": obj.id, })
    #     return format_html(f"<a href=\"{link}?response=html\">{link}</a>")

    def get_fieldsets_dict(self, request, obj=None):
        default_fieldsets_dict = super().get_fieldsets_dict(request, obj)
        default_fieldsets_dict[self.lookup_general_key]["value"]["fields"] = ["title", "builder_type", "related"]
        if obj is None:
            return default_fieldsets_dict
        default_fieldsets_dict.update(
            {
                "content": {
                    "label": "Content",
                    "value": {
                        "fields": (
                            # "use_ssr_render",
                            # "preview_url",
                            "styles",
                            "content_json",
                        ),
                    }
                }
            },
        )
        self.lookup_key_list = [self.lookup_general_key, "content", self.lookup_important_dated_key, ]
        return default_fieldsets_dict
