from django.apps import AppConfig


class FileSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.file_system'

    def ready(self):
        import apps.file_system.signals
