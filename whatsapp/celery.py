import os
from celery import Celery
import logging
import eventlet
# eventlet.monkey_patch()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whatsapp.settings")
app = Celery("whatsapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# logging.basicConfig(filename='celery.log', level=logging.INFO)
# 
# celery = Celery('tasks', broker='redis://localhost:6379/0')


# @app.task(bind=True)
# def debug_task(self):
#     printf(f"request: {self.request!r}")
