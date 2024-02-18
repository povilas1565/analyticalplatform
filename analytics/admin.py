from django.contrib import admin

from .models import Wallet, Transaction, Coin, WalletStat, Whale

admin.site.register(Transaction)
admin.site.register(Coin)
admin.site.register(WalletStat)
admin.site.register(Whale)

class TransactionFrom(admin.TabularInline):
    model = Transaction
    extra = 1
    fk_name = "from_wallet"


@admin.register(Wallet)
class PostAdmin(admin.ModelAdmin):
    inlines = [TransactionFrom]