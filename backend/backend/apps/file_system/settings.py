from django.conf import settings

THUMBNAIL_SIZES = getattr(
    settings, "FILE_SYSTEM_THUMBNAIL_SIZES", ((60, 60), (100, 100), (200, 200), (300, 300), (400, 400), (600, 600))
)