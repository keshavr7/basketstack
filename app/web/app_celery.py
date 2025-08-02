from __future__ import absolute_import, unicode_literals

import logging
import os

from celery import Celery
from celery.signals import setup_logging

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
celery_app = Celery("web")

# Only import setting module after we have configured DJANGO_SETTINGS_MODULE env variable.

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig

    from django.conf import settings

    logging_settings = settings.LOGGING

    dictConfig(logging_settings)


# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()
