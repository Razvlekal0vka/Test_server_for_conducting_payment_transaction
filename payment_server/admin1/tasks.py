from celery import shared_task
from django.utils import timezone
from .models import Invoice

@shared_task
def check_invoice_expiration(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    if invoice.status == 'ожидает оплату' and invoice.expiration_date < timezone.now():
        invoice.status = 'просрочен'
        invoice.save()
