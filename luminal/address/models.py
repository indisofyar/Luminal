from django.db import models


class Address(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True, unique=True)
    last_synced = models.DateTimeField(null=True)
    last_block_number = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.address:
            return self.address
        else:
            return str(self.id)

class Transaction(models.Model):
    transaction_hash = models.CharField(max_length=255, primary_key=True)
    block_number = models.CharField(max_length=255)  # Changed to CharField
    status = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name='main_address')
    from_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name='from_transactions')
    to_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name='to_transactions')
    method = models.CharField(max_length=255, blank=True, null=True)
    tx_type = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    gas_used = models.BigIntegerField()  # Changed to CharField
    priority_fee = models.BigIntegerField()  # Changed to CharField
    base_fee_per_gas = models.BigIntegerField()  # Changed to CharField
    total_gas_paid = models.DecimalField(decimal_places=5, max_digits=15)  # Changed to CharField
    error_status = models.CharField(max_length=255, blank=True, null=True)
    revert_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transaction_hash
