from django.contrib import admin

from order.models import Currency, Order


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'price', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "currency", "amount", "state", "is_partial", ]
    list_filter = ["state", "is_partial", ]
    readonly_fields = ["user", "currency", ]
