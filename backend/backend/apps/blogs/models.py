from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel

from utils.models import AbstractTimestampedModel, AbstractMetaModel

UserModel = get_user_model()


class BlogPostCategory(AbstractTimestampedModel):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)


class BlogPostStatus(models.IntegerChoices):
    DRAFT = 0, "Draft"
    PUBLISH = 1, "Publish"


class BlogPost(AbstractTimestampedModel, AbstractMetaModel, SoftDeleteModel):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                               related_name='blog_posts')
    category = models.ForeignKey(
        BlogPostCategory, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    status = models.IntegerField(
        choices=BlogPostStatus.choices, default=BlogPostStatus.DRAFT)
    page = models.OneToOneField('pages.PageDocument', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.title,
                               self.category)


class BlogComment(AbstractTimestampedModel):
    blog = models.ForeignKey(BlogPost, null=True, blank=True, on_delete=models.SET_NULL, related_name="comments", )
    author = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.SET_NULL, related_name="comments", )
    title = models.CharField(_("Title"), max_length=50)
    message = models.TextField(_("Message"), max_length=500)

    def __str__(self):
        return '{}, {}, {}'.format(self.blog, self.author, self.title)
