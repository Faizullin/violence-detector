from django.urls import path
from apps.carts import views

urlpatterns = [
    path('api/v1/', views.view_cart, name='view_cart'),
    path('api/v1/add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/v1/adjust/<item_id>/', views.adjust_cart, name='adjust_cart'),
    path('api/v1/remove/<item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
