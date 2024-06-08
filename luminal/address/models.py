from django.db import models

class Transaction(models.Model):
    transaction_hash = models.CharField(max_length=255, primary_key=True)
    block_number = models.IntegerField()
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    from_address = models.CharField(max_length=255, blank=True, null=True)
    to_address = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    tx_type = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    gas_used = models.IntegerField()
    priority_fee = models.IntegerField()
    base_fee_per_gas = models.IntegerField()
    total_gas_paid = models.IntegerField()
    error_status = models.CharField(max_length=255, blank=True, null=True)
    revert_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transaction_hash