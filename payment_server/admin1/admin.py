from django.contrib import admin
from .models import Invoice, PaymentAttempt
from .tasks import check_invoice_expiration
from django.utils.html import format_html
from django.http import HttpRequest
from django.db.models import Model
from typing import Any, Optional

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    exclude = ("invoice_id",)

    list_display = (
        "invoice_id",
        "amount",
        "created_at",
        "status",
        "colored_status",
        "expiration_date",
    )
    list_filter = ("status",)

    def save_model(self, request, obj, form, change):
        text = f"invoice_id {obj.invoice_id}, amount {obj.amount}, expiration_date {obj.expiration_date}, status {obj.status}, created_at {obj.created_at}"

        super().save_model(request, obj, form, change)
        if obj.status == "ожидает оплату":
            print(
                f"Scheduling check_invoice_expiration for invoice {obj.id} at {obj.expiration_date}"
            )
            check_invoice_expiration.apply_async()

    def colored_status(self, obj: Model) -> str:
        if obj.status == "ожидает оплату":
            color = "yellow"
        elif obj.status == "оплачен":
            color = "green"
        elif obj.status == "просрочен":
            color = "red"
        else:
            color = "black"
        return format_html('<span style="color: {};">{}</span>', color, obj.status)

    colored_status.short_description = "Status"


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ("invoice", "status", "attempt_id", "amount")

    def save_model(self, request: HttpRequest, obj: Model, form: Any, change: bool) -> None:
        print(
            f"invoice {obj.invoice}, attempt_id {obj.attempt_id}, status {obj.status}, amount {obj.amount}"
        )

        check_invoice_expiration.apply_async()
        if obj.invoice.status == "ожидает оплату":
            if obj.amount < obj.invoice.amount:
                obj.status = "недостаточно средств"
            else:
                obj.status = "успешно"
                obj.invoice.status = "оплачен"
                obj.invoice.save()
        elif obj.invoice.status == "просрочен":
            obj.status = "отказ"
        super().save_model(request, obj, form, change)
