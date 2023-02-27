import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showroom_project.settings")

app = Celery("showroom_project")


app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()
app.conf.timezone = "UTC"
app.conf.beat_schedule = {
    "client_buy": {
        "task": "showroom.tasks.client_buy_car_from_showroom",
        "schedule": crontab(minute="*/6"),
    },
    "showroom_buy": {
        "task": "showroom.tasks.showroom_buy_car",
        "schedule": crontab(minute="*/1"),
    },
}
