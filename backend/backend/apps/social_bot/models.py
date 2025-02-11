from django.contrib.auth import get_user_model

from utils.models import models, AbstractTimestampedModel

UserModel = get_user_model()


class SocialUser(AbstractTimestampedModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    tg_chat_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=True, blank=True)
