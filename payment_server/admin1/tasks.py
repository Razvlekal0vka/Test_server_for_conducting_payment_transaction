from celery import shared_task
from django.utils import timezone
from .models import Invoice
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_invoice_expiration(invoice_id):
    logger.info(f"Checking expiration for invoice {invoice_id}")
    invoice = Invoice.objects.get(id=invoice_id)
    if invoice.status == 'ожидает оплату' and invoice.expiration_date < timezone.now():
        invoice.status = 'просрочен'
        invoice.save()
