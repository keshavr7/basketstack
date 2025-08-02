# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import, unicode_literals

from .app_celery import celery_app

__all__ = ("celery_app",)
