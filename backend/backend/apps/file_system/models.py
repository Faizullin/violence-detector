from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import AbstractTimestampedModel
from .fields import ImageWithThumbsField
from .settings import THUMBNAIL_SIZES


def upload_file_name(self, filename):
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
    file_name_split = filename.split('.')
    file_name_list = file_name_split[:-1]
    ext = file_name_split[-1]
    file_name_wo_ext = '.'.join(file_name_list)
    return 'files/{0}__{1}.{2}'.format(file_name_wo_ext, datetime_str, ext)


class AbstractFileModel(models.Model):
    name = models.CharField(_("Name"), blank=True, max_length=100)
    alt = models.CharField(_("Alt"), blank=True, max_length=255)
    url = models.URLField(_("URL"), blank=True, max_length=255)

    class Meta:
        abstract = True
        ordering = ("-id",)

    def __str__(self):
        return self.name

    def get_alt(self):
        if self.alt:
            return self.alt
        return self.name


class Image(AbstractFileModel, AbstractTimestampedModel):
    image = ImageWithThumbsField(_("Image"), upload_to=upload_file_name, blank=True, null=True, sizes=THUMBNAIL_SIZES)


class File(AbstractFileModel, AbstractTimestampedModel):
    file = models.FileField(_("File"), upload_to=upload_file_name, null=True, blank=True)
