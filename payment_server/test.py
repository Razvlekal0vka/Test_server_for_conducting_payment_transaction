from admin1 import tasks
from django.utils import timezone
from datetime import datetime, timedelta

print({'invoice_id': 10})

tasks.check_invoice_expiration.applay_async(args={'invoice_id': 10}, eta=timedelta(seconds=+20))