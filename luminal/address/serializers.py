from rest_framework import serializers
from .models import Address, Transaction

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'address']

class TransactionSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    from_address = AddressSerializer()
    to_address = AddressSerializer()

    class Meta:
        model = Transaction
        fields = ['transaction_hash', 'block_number', 'status', 'address', 'from_address', 'to_address', 'method', 'tx_type', 'timestamp', 'gas_used', 'priority_fee', 'base_fee_per_gas', 'total_gas_paid', 'error_status', 'revert_reason']
