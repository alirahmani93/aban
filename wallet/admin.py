from django.contrib import admin

from wallet.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "currency", "is_active", 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ["user", "currency"]
