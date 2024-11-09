from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class AbstractMetaModel(models.Model):
    meta_title = models.CharField(_("Meta title"), blank=True, max_length=80)
    meta_keywords = models.CharField(_("Meta keywords"), blank=True, max_length=255)
    meta_description = models.TextField(_("Meta description"), blank=True)
    use_ssr = models.BooleanField(_("Use SSR"), default=False)
    render_url = models.CharField(_("Render URL"), blank=True, max_length=80)

    class Meta:
        abstract = True


class AbstractActiveModel(models.Model):
    is_active = models.BooleanField(_("Active"), default=False)

    class Meta:
        abstract = True