import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object(settings, namespace="CELERY")

app.conf.beat_schedule = {
    "update-currencies-every-hour": {
        "task": "currency.tasks.update_currency",
        "schedule": crontab(minute="*/1"),
    }
}

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
