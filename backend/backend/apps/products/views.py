from django.conf import settings
from django.db.models import Prefetch
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductListPagination, ProductListFilter
from .models import Product, ProductBrand, ProductCategory, Offer
from .serializers import ProductListSerializer, ProductRetrieveSerializer, ProductBrandSerializer, \
    ProductCategorySerializer, OfferSerializer
from .utils import get_filters_cache


class ProductListFiltersApiView(APIView):
    def get(self, request):
        cache_key, cache, data = get_filters_cache()
        if not data:
            brands = ProductBrand.objects.filter(is_active=True)
            categories = ProductCategory.objects.filter(is_active=True)
            offers = Offer.objects.filter(is_active=True)
            data = {
                "brands": ProductBrandSerializer(brands, many=True).data,
                "categories": ProductCategorySerializer(categories, many=True).data,
                "offers": OfferSerializer(offers, many=True).data
            }
            cache.set(cache_key, data, timeout=60)
        return Response(data, status=status.HTTP_200_OK)


class ProductRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = ProductRetrieveSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductListApiView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filterset_class = ProductListFilter
    pagination_class = ProductListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['name', 'short_description']

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch('brand', queryset=ProductBrand.objects.filter(is_active=True)),
            Prefetch('category', queryset=ProductCategory.objects.filter(is_active=True)),
            Prefetch('offer', queryset=Offer.objects.filter(is_active=True)),
        ).filter(is_active=True)


class ProductRetrieveRenderView(DetailView):
    lookup_field = 'slug'
    template_name = 'products/product_detail.html'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "FRONTEND_APP_BASE_URL": settings.FRONTEND_APP_BASE_URL,
        })
        return context
