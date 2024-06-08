from django.contrib import admin

from .models import Transaction, Address


class AddressAdmin(admin.ModelAdmin):
    pass

class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Address, AddressAdmin)