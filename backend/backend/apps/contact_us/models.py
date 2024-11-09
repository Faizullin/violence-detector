from django.db import models
from django.utils.text import gettext_lazy as _

from utils.models import AbstractTimestampedModel


class ContactDetail(AbstractTimestampedModel):
    name = models.CharField(_('Username'), max_length=100)
    subject = models.CharField(_('Subject'), max_length=255)
    phone = models.CharField(_('Phone Number'), max_length=15, null=True)
    email = models.EmailField(_('Email Address'), null=True)
    message = models.TextField(_('Message'), )

    def __str__(self):
        return f"Subject: {self.subject}, Email: {self.email}, Name: {self.name}"

    class Meta:
        unique_together = ('created_at', 'name')
        verbose_name = _('Contact Detail')
        verbose_name_plural = _('Contact Details')
