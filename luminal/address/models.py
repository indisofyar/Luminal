from django.db import models

class Transaction(models.Model):
    transaction_hash = models.CharField(max_length=255, primary_key=True)
    block_number = models.CharField(max_length=255)  # Changed to CharField
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    from_address = models.CharField(max_length=255, blank=True, null=True)
    to_address = models.CharField(max_length=255, blank=True, null=True)
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
