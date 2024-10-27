from celery import shared_task
from django.utils import timezone
from .models import Invoice
import logging
from typing import NoReturn

logger = logging.getLogger(__name__)


@shared_task
def check_invoice_expiration() -> NoReturn:
    logger.info("Checking expiration for all invoices")
    invoices = Invoice.objects.filter(
        status="ожидает оплату", expiration_date__lt=timezone.now()
    )
    for invoice in invoices:
        invoice.status = "просрочен"
        invoice.save()
