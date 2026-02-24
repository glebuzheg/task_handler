import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

if getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False):
    app.conf.task_always_eager = True

