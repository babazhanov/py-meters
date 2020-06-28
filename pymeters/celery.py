import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymeters.settings')

celery_app = Celery('pymeters',
                    backend='redis://localhost',
                    broker='redis://localhost')

celery_app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks(['station'])
"""
celery_app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'publisher.tasks.send_view_count_report',
        'schedule': crontab(minute=48, hour=21),
    },
}
"""
