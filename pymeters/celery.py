import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymeters.settings')
#os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

celery_app = Celery('pymeters',
                    backend='redis://127.0.0.1:6379/0',
                    broker='redis://127.0.0.1:6379/0')

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
# логирование celery
# celery_app.log.setup(loglevel='info', logfile='celery.log')
