import os

from celery import Celery
from celery.schedules import schedule

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payment_server_admin_panel2.settings")

app = Celery("payment_server_admin_panel2")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-invoice-expiration-admin2": {
        "task": "admin2.tasks.check_invoice_expiration",
        "schedule": 60.0,
        "args": (),
    },
}



@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
