import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aban.settings.settings')
app = Celery("aban")

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_transport_options = {'visibility_timeout': 72000}  # 20*3600

SHORT_TERMINAL_TIMEDELTA=5

# Queues
DEFAULT_QUEUE = 'celery'
ORDER_QUEUE = 'order'

GENERAL_RETRY_POLICY = {
    'autoretry_for': (Exception,),
    'retry_backoff': 5,
    'retry_jitter': True,
    'retry_kwargs': {'max_retries': 3, 'countdown': 10},
}
