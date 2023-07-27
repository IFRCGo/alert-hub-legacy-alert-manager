import os
from celery import Celery
from django.conf import settings
from dotenv import load_dotenv
from kombu import Queue
# Load environment variables from .env file
if 'WEBSITE_HOSTNAME' not in os.environ:
    load_dotenv(".env")
    # Set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alertmanager.settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alertmanager.production')
app = Celery('alertmanager')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.task_default_queue = 'cache'
app.conf.task_queues = (
    Queue('cache', routing_key='cache.#', exchange='cache'),
)
app.conf.task_default_exchange = 'cache'
app.conf.task_default_exchange_type = 'topic'
app.conf.task_default_routing_key = 'cache.default'

task_routes = {
        'alert_cache.tasks.*': {
            'queue': 'cache',
            'routing_key': 'cache.#',
            'exchange' : 'cache',
        },
}