from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django_softdelete.models import SoftDeleteModel

from apps.file_system.fields import ImageWithThumbsField
from utils.models import AbstractTimestampedModel, models


def upload_profile_file(self, filename):
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
    file_name_split = filename.split('.')
    file_name_list = file_name_split[:-1]
    ext = file_name_split[-1]
    file_name_wo_ext = '.'.join(file_name_list)
    return 'profiles/{0}__{1}.{2}'.format(file_name_wo_ext, datetime_str, ext)


class CustomUser(AbstractUser, SoftDeleteModel):
    pass


class UserProfile(AbstractTimestampedModel, SoftDeleteModel):
    user = models.OneToOneField(
        CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name="profile")
    default_email = models.EmailField(max_length=254, null=False, blank=False)
    default_postcode = models.CharField(max_length=20, null=False, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=False,
                                            blank=True)
    default_address_line_1 = models.CharField(max_length=80, null=False,
                                              blank=True)
    default_address_line_2 = models.CharField(max_length=80, null=False,
                                              blank=True)
    default_county = models.CharField(max_length=80, null=False, blank=True)
    image = ImageWithThumbsField(
        upload_to=upload_profile_file, sizes=((200, 200,),), null=True, blank=True, )

    def __str__(self):
        return '{}, {}'.format(self.user,
                               self.default_email)
