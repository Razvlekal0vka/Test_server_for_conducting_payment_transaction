from django.contrib import admin
from .models import Invoice, PaymentAttempt
from .tasks import check_invoice_expiration


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    exclude = ('invoice_id',)

    list_display = ('invoice_id', 'amount', 'created_at', 'status', 'expiration_date')

    def save_model(self, request, obj, form, change):
        text = f"invoice_id {obj.invoice_id}, amount {obj.amount}, expiration_date {obj.expiration_date}, status {obj.status}, created_at {obj.created_at}"
        print('=' * len(text))
        print(text)
        print('=' * len(text))

        super().save_model(request, obj, form, change)
        if obj.status == 'ожидает оплату':
            print(f"Scheduling check_invoice_expiration for invoice {obj.id} at {obj.expiration_date}")
            check_invoice_expiration.apply_async(args=[obj.id], eta=obj.expiration_date)
            print(1)


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_id', 'invoice', 'status', 'created_at', 'amount')

    def save_model(self, request, obj, form, change):
        print(f"invoice {obj.invoice}, attempt_id {obj.attempt_id}, status {obj.status}, amount {obj.amount}, created_at {obj.created_at}")

        if obj.invoice.status == 'ожидает оплату':
            if obj.amount > obj.invoice.amount:
                obj.status = 'недостаточно средств'
            else:
                obj.status = 'успешно'
                obj.invoice.status = 'оплачен'
                obj.invoice.save()
        elif obj.invoice.status == 'просрочен':
            obj.status = 'отказ'
        super().save_model(request, obj, form, change)
