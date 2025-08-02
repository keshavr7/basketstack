import multiprocessing
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

from django.conf import settings

bind = "0.0.0.0:8000"
reload = True
workers = 4 if settings.DEBUG else min(multiprocessing.cpu_count() * 2 + 1, 8)
accesslog = "-"
access_log_format = (
    '%(t)s %(p)s [%(s)s] %(h)s %(u)s "%(r)s" [%(D)s microsec] [%(b)s byte] "%(f)s" "%(a)s"'
)
