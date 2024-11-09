from django_filters import rest_framework as django_filters
from apps.notification_system.models import Notification
from rest_framework.pagination import PageNumberPagination


class BasicPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 30


class NotificationFilter(django_filters.FilterSet):  
    # title = django_filters.CharFilter(
    #     field_name="translations__title", lookup_expr='exact')
    # title__contains = django_filters.CharFilter(
    #     field_name="translations__title", lookup_expr='contains')     
    ordering = django_filters.OrderingFilter(
        fields=(
            'id', 'author__username', 'created_at', 'updated_at',
        )
    )
    
    class Meta:
        model = Notification
        fields = {
            'id': ['exact',],
            'unread': ['exact',],
            'created_at': ['exact', 'date', 'lt', 'gt'],
            'updated_at': ['exact', 'date', 'lt', 'gt'],
        }


class SoftDeletedItemFilter(django_filters.FilterSet):
    # title = django_filters.CharFilter(
    #     field_name="translations__title", lookup_expr='exact')
    # title__contains = django_filters.CharFilter(
    #     field_name="translations__title", lookup_expr='contains')
    ordering = django_filters.OrderingFilter(
        fields=(
            'id', 'author__username', 'created_at', 'updated_at',
        )
    )

    class Meta:
        model = Notification
        fields = {
            'id': ['exact', ],
            'unread': ['exact', ],
            'created_at': ['exact', 'date', 'lt', 'gt'],
            'updated_at': ['exact', 'date', 'lt', 'gt'],
        }