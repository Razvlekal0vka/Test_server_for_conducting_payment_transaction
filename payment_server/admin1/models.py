from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    # Уникальный идентификатор счета на оплату
    invoice_id = models.CharField(max_length=100, unique=True)
    # Сумма счета на оплату
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Валюта счета на оплату
    currency = models.CharField(max_length=3)
    #Срок оплаты (истечение)
    expiration_date = models.DateTimeField(default=timezone.now)
    # Статус счета
    status = models.CharField(max_length=20, default='ожидает оплату')
    # Описание счета на оплату
    description = models.TextField(blank=True)
    # Дата и время создания счета на оплату
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата и время последнего обновления счета на оплату
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_id

class PaymentAttempt(models.Model):
    # Внешний ключ, связывающий попытку оплаты с определенным счетом на оплату
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payment_attempts')
    # Уникальный идентификатор попытки оплаты
    attempt_id = models.CharField(max_length=100, unique=True)
    # Статус попытки оплаты
    status = models.CharField(max_length=20)
    #Деньги
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Сообщение, связанное с попыткой оплаты
    message = models.TextField(blank=True)
    # Дата и время создания попытки оплаты
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата и время последнего обновления попытки оплаты
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.attempt_id
