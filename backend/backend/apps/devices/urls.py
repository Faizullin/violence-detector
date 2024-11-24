from django.urls import path

from .views import DeviceListView, DeviceCreateView, DeviceUpdateView

app_name = 'devices'

urlpatterns = [
    path('device/list/my', DeviceListView.as_view(), name='device-list-my'),
    path('device/create/', DeviceCreateView.as_view(), name='device-create'),
    path('device/<int:pk>/edit/', DeviceUpdateView.as_view(), name='device-update'),
    # path('device/<int:pk>/regenerate-api-key/', APIKeyRegenerateView.as_view(), name='api_key_regenerate'),
]
