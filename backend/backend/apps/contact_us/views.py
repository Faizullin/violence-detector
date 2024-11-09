from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from .serializers import ContactFormSerializer, ContactDetail


class ContactAnonymousUserRateThrottle(UserRateThrottle):
    rate = '1/min'


class SubmitContactFormView(generics.CreateAPIView):
    queryset = ContactDetail.objects.all()
    serializer_class = ContactFormSerializer
    throttle_classes = [ContactAnonymousUserRateThrottle]
