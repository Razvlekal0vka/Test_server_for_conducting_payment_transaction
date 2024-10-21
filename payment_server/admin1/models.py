from django.db import models
from django.utils import timezone
import uuid
from django.db.models import Max

import time
import random


class Invoice(models.Model):
    # Уникальный идентификатор счета на оплату
    invoice_id = models.CharField(max_length=100, unique=True, editable=False)
    # Сумма счета на оплату
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Валюта счета на оплату
    expiration_date = models.DateTimeField(default=timezone.now)
    # Статус счета
    status = models.CharField(max_length=20, default='ожидает оплату')
    # Дата и время создания счета на оплату
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_invoice = Invoice.objects.aggregate(Max('invoice_id'))['invoice_id__max']
            if last_invoice is not None:
                self.invoice_id = str(int(last_invoice) + 1)
            else:
                self.invoice_id = '1'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_id


class PaymentAttempt(models.Model):
    # Внешний ключ, связывающий попытку оплаты с определенным счетом на оплату
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payment_attempts')
    # Уникальный идентификатор попытки оплаты
    attempt_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    # Статус попытки оплаты
    status = models.CharField(max_length=20)
    # Вносимая сумма
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Дата и время создания попытки оплаты
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.attempt_id
