from django.contrib import admin
from .models import PaymentHistory, PaymentSession, WalletAmountSession


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'course', 'amount', 'is_success', 'get_created_at')
    list_filter = ('user', 'package', 'course',  'is_success')


admin.site.register(PaymentSession)
admin.site.register(WalletAmountSession)