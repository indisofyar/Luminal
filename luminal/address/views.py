from django.db import IntegrityError
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.utils.dateparse import parse_datetime

from address.models import Transaction


# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response('Hello world')


@api_view(['GET'])
def get_data(request, address):
    url = "https://evm-sidechain.xrpl.org/api/v2/addresses/" + address + "/transactions"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        transactions = []
        next_page_params = data.get("next_page_params")
        block_number = next_page_params.get("block_number")
        page=next_page_params.get("page")

        for item in data.get('items', []):
            if Transaction.objects.filter(transaction_hash=item.get('hash', '')).exists():
                # If a transaction already exists, break the loop to stop processing
                break
            
            transaction = Transaction(
                transaction_hash=item.get('hash', ''),
                block_number=item.get('block', 0),
                address=address,
                status=item.get('status', ''),
                from_address=item.get('from_address'),
                to_address=item.get('to_address'),
                method=item.get('method', ''),
                tx_type=item.get('tx_types', )[0],
                timestamp=parse_datetime(item.get('timestamp')),
                gas_used=int(item.get('gas_used', 0)),
                priority_fee=int(item.get('priority_fee', 0)),
                base_fee_per_gas=int(item.get('base_fee_per_gas', 0)),
                total_gas_paid=(int(item.get('base_fee_per_gas', 0)) + int(item.get('priority_fee', 0))) * int(
                    item.get('gas_used', 0)),
                error_status=item.get('result', ''),
                revert_reason=item.get('revert_reason', '')
            )
            transactions.append(transaction)

            try:
                transaction.save()
            except IntegrityError:
                break  # Stop if transaction already exists (handles race conditions)

        # Serializing data
        transaction_data = []
        for txn in transactions:
            transaction_data.append({
                'transaction_hash': txn.transaction_hash,
                'block_number': txn.block_number,
                'address': txn.address,
                'status': txn.status,
                'from_address': txn.from_address,
                'to_address': txn.to_address,
                'method': txn.method,
                'tx_type': txn.tx_type,
                'timestamp': txn.timestamp,
                'gas_used': txn.gas_used,
                'priority_fee': txn.priority_fee,
                'base_fee_per_gas': txn.base_fee_per_gas,
                'total_gas_paid': txn.total_gas_paid,
                'error_status': txn.error_status,
                'revert_reason': txn.revert_reason
            })

            Transaction.objects.get_or_create(
                transaction_hash=txn.transaction_hash,
                defaults={
                    'block_number': txn.block_number,
                    'address': txn.address,
                    'status': txn.status,
                    'from_address': txn.from_address,
                    'to_address': txn.to_address,
                    'method': txn.method,
                    'tx_type': txn.tx_type,
                    'timestamp': txn.timestamp,
                    'gas_used': txn.gas_used,
                    'priority_fee': txn.priority_fee,
                    'base_fee_per_gas': txn.base_fee_per_gas,
                    'total_gas_paid': txn.total_gas_paid,
                    'error_status': txn.error_status,
                    'revert_reason': txn.revert_reason
                }
            )

        return Response(transaction_data, status=status.HTTP_200_OK)
    except requests.exceptions.HTTPError as http_err:
        return Response({"error": str(http_err)}, status=response.status_code)
    except requests.exceptions.RequestException as err:
        return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)