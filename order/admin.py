from django.contrib import admin
from .models import Order, OrderItem, Discount

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['package', 'course']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'paid_at')
    list_filter = ('user',  'created_at', 'paid_at')
    search_fields = ('user', )
    inlines = [OrderItemInline]


admin.site.register(Discount)
