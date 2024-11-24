from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('blogs/<int:id>/', views.blog_detail, name='blog_detail'),
]