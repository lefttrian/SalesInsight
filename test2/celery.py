import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test2.settings')

app = Celery('test2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()