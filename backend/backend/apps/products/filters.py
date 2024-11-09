import django_filters.rest_framework as django_filters
from rest_framework.pagination import PageNumberPagination

from .models import Product


class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 30


class ProductListFilter(django_filters.FilterSet):
    categories = django_filters.BaseInFilter(field_name='category')
    brands = django_filters.BaseInFilter(field_name='brand')
    offer = django_filters.CharFilter(lookup_expr='exact', field_name='offer')
    price = django_filters.RangeFilter(field_name='price_of_offer')
    offer__discount = django_filters.RangeFilter(field_name='offer__discount', lookup_expr='gte')
    ordering = django_filters.OrderingFilter(
        fields=(

        )
    )

    class Meta:
        model = Product
        fields = ['brands', 'categories', 'offer', 'price', 'offer__discount']
