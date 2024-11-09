from rest_framework import serializers
from .models import ContactDetail


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = ['name', 'subject', 'phone', 'email', 'message']