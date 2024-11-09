from django.urls import path

from .views import SubmitContactFormView

app_name = 'contact_us'

urlpatterns = [
    path('api/v1/contact_us/submit/', SubmitContactFormView.as_view(), name='contact_us-submit'),
]
