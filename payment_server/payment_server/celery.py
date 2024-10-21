import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_server.settings')

app = Celery('payment_server')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


#@app.task(bind=True, ignore_result=True)
#def debug_task(self):
    #print(f'Request: {self.request!r}')

# celery -A payment_server flower

# python manage.py makemigrations
# python manage.py migrate

# python manage.py migrate --run-syncdb

# python manage.py createsuperuser

# python manage.py runserver

# celery -A payment_server worker --loglevel=INFO --pool=solo

# celery.py

from celery.schedules import schedule

app.conf.beat_schedule = {
    'check-invoice-expiration-every-second': {
        'task': 'admin1.tasks.check_invoice_expiration',
        'schedule': schedule(run_every=1),  # Проверять каждую секунду
    },
}

# celery -A payment_server worker -l info
# celery -A payment_server beat -l info