from utils.models import AbstractTimestampedModel, models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Blog(AbstractTimestampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)

