from django.contrib import admin
from .models import Invoice, PaymentAttempt
from .tasks import check_invoice_expiration

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'amount', 'currency', 'created_at', 'updated_at', 'status', 'expiration_date')
    search_fields = ('invoice_id', 'description')
    list_filter = ('currency', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == 'ожидает оплату':
            print(f"Scheduling check_invoice_expiration for invoice {obj.id} at {obj.expiration_date}")
            check_invoice_expiration.apply_async(args=[obj.id], eta=obj.expiration_date)


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_id', 'invoice', 'status', 'created_at', 'updated_at')
    search_fields = ('attempt_id', 'message')
    list_filter = ('status', 'created_at')

    def save_model(self, request, obj, form, change):
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