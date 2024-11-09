from django.contrib import admin
from django_restful_admin import admin as api_admin
from rest_framework.viewsets import ModelViewSet

from utils.admin import BaseAdmin
from utils.pagination import DefaultPageNumberWithPageSizePagination
from .models import (BlogComment, BlogPost, BlogPostCategory)
from ..accounts.permissions import permissions, IsAdminOrStaffOrDevloper
from ..pages.models import PageDocument, BuilderType


@api_admin.register(BlogPost)
class BlogPostApiAdmin(ModelViewSet):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStaffOrDevloper]
    pagination_class = DefaultPageNumberWithPageSizePagination


@admin.register(BlogPost)
class BlogAdmin(BaseAdmin):
    list_display = ('title', 'slug', 'status',)
    list_filter = ("status", 'category')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author', 'page')

    def save_model(self, request, obj: BlogPost, form, change):
        if change == False:
            if not obj.page:
                page_title = obj.title
                obj.page = PageDocument.objects.create(
                    title=page_title,
                    builder_type=BuilderType.PUCK_DB_JSON,
                    content_json='{"root": {"props": {"title": "' + page_title + '"}}, "content": []}',
                    related=True,
                )
            obj.save()
            return obj
        else:
            obj.save()


@admin.register(BlogComment)
class BlogCommentAdmin(BaseAdmin):
    list_display = ('title', 'message',)
    search_fields = ['message']


@admin.register(BlogPostCategory)
class BlogPostCategoryAdmin(BaseAdmin):
    list_display = ('title', 'slug',)
    search_fields = ['title', ]
