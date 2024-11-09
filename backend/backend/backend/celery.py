# celery.py

from __future__ import absolute_import, unicode_literals

import os
from logging.config import dictConfig

import celery.signals
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

app = Celery('backend')
# app.conf.enable_utc = False
# app.conf.update(timezone = 'Asia/Almaty')

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')


@celery.signals.worker_ready.connect
def configure_logging(sender=None, conf=None, **kwargs):
    print("@celery.worker_ready.connect", settings.LOGGING.keys())
    dictConfig(settings.LOGGING)

# @celery.signals.setup_logging.connect
# def config_loggers(*args, **kwags):
#     print("@celery.signals.setup_logging.connect", settings.LOGGING.keys())
#     dictConfig(settings.LOGGING)


# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
