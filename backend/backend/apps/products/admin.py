from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Product, ProductReview, ProductCategory, Offer, ProductBrand


@admin.register(Offer)
class OfferAdmin(BaseAdmin):
    list_display = ('name', 'discount', 'is_active', 'valid_from', 'valid_to')
    list_filter = ('valid_from', 'is_active', 'valid_from', 'valid_to')
    search_fields = ['name', 'discount']


@admin.register(ProductBrand)
class ProductBrandAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug',)
    list_filter = ()
    search_fields = ['name', 'slug']


@admin.register(ProductCategory)
class ProductCategoryAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug',)
    list_filter = ()
    search_fields = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'category', 'base_price', 'price_of_offer', 'is_active',)
    list_filter = ("category", 'is_active',)
    search_fields = ['name', ]


@admin.register(ProductReview)
class ProductReviewAdmin(BaseAdmin):
    list_display = ('title', 'product', 'author', 'score', 'created_at',)
    search_fields = ['title', ]
