from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('api/v1/products/filters/', views.ProductListFiltersApiView.as_view(), name='product-list-filters-api'),
    path('api/v1/products/', views.ProductListApiView.as_view(), name='product-list-api'),
    path('api/v1/products/<slug:slug>/', views.ProductRetrieveApiView.as_view(), name='product-retrieve-api'),
    path('s/products/<slug:slug>/', views.ProductRetrieveRenderView.as_view(), name='product-retrieve-render'),
]
