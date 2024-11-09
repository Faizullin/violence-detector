from django.urls import path

from .views import (BlogListApiView, BlogDetailApiView)

app_name = 'blogs'

urlpatterns = [
    path('api/v1/blogs/', BlogListApiView.as_view(), name='blog-list-api'),
    path('api/v1/blogs/<slug:slug>/', BlogDetailApiView.as_view(), name='blog-retrieve-api'),
]
