from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'showroom_project.settings')
app = Celery('showroom_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()