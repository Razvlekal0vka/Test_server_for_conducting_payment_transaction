from django.db import models
from django.utils import timezone
from django.db.models import Max


class Invoice(models.Model):
    # Уникальный идентификатор счета на оплату
    invoice_id = models.CharField(max_length=100, unique=True, editable=False)
    # Сумма счета на оплату
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Time
    expiration_date = models.DateTimeField(default=timezone.now)
    # Статус счета
    status = models.CharField(max_length=20, default="ожидает оплату", editable=False)
    # Дата и время создания счета на оплату
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        if not self.invoice_id:
            last_invoice = Invoice.objects.aggregate(Max("invoice_id"))[
                "invoice_id__max"
            ]
            if last_invoice is not None:
                self.invoice_id = str(int(last_invoice) + 1)
            else:
                self.invoice_id = "1"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.invoice_id


class PaymentAttempt(models.Model):
    # Внешний ключ, связывающий попытку оплаты с определенным счетом на оплату
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payment_attempts"
    )
    # Уникальный идентификатор попытки оплаты
    attempt_id = models.CharField(max_length=100, unique=True, editable=False)
    # Статус попытки оплаты
    status = models.CharField(max_length=20, default="", editable=False)
    # Вносимая сумма
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs) -> None:
        if not self.attempt_id:
            last_attempt = PaymentAttempt.objects.aggregate(Max("attempt_id"))[
                "attempt_id__max"
            ]
            if last_attempt is not None:
                self.attempt_id = str(int(last_attempt) + 1)
            else:
                self.attempt_id = "1"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.attempt_id
