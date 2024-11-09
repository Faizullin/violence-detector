from django_softdelete.models import SoftDeleteModel

from utils.models import AbstractTimestampedModel, AbstractMetaModel, models


class PageStyle(AbstractTimestampedModel):
    title = models.CharField(max_length=100, default="")
    content = models.TextField(null=True, blank=True)


class BuilderType(models.TextChoices):
    PUCK_DB_JSON = "PUCK_DB_JSON", "puck_db_json"
    PUCK_LOCAL_HTML = "PUCK_LOCAL_HTML", "puck_local_html"


class PageDocument(AbstractTimestampedModel, AbstractMetaModel, SoftDeleteModel):
    title = models.CharField(max_length=100)
    builder_type = models.CharField(max_length=100, choices=BuilderType.choices, default=BuilderType.PUCK_DB_JSON)
    local_path = models.FileField(default=None, null=True, blank=True)
    content_json = models.TextField(null=True, blank=True)
    related = models.BooleanField(default=False)
    styles = models.ManyToManyField(PageStyle, blank=True)
    # html = GrapesJsHtmlField()
