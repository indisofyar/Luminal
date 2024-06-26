from django.db import IntegrityError
from django.db.models import Sum, Avg, Q
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from django.utils.dateparse import parse_datetime

from address.models import Transaction

from .models import Address
from .serializers import TransactionSerializer, AddressSerializer


# Create your views here.
@api_view(['GET'])
def health_check(request):
    return Response('Health check succeeded')


@api_view(['GET'])
def sync_data(request, address, name=None):
    url = "https://evm-sidechain.xrpl.org/api/v2/addresses/" + address + "/transactions"
    headers = {
        "Content-Type": "application/json"
    }

    if name:
        name = name.split('-')
        for i in range(len(name)):
            name[i] = name[i].capitalize()
        name = ' '.join(name)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        transactions = []
        next_page_params = data.get("next_page_params")
        block_number = next_page_params.get("block_number")
        page = next_page_params.get("page")

        for item in data.get('items', []):

            main_address, created = Address.objects.get_or_create(address=address)

            found_from_address = item.get('from')
            found_to_address = item.get('to')

            from_address = None
            to_address = None

            if found_from_address:
                from_address, created = Address.objects.get_or_create(address=found_from_address['hash'])
            if found_to_address:
                to_address, created = Address.objects.get_or_create(address=found_to_address['hash'])

            if name is not None:
                if from_address.address == address:
                    from_address.name = name
                    from_address.save()
                elif to_address.address == address:
                    to_address.name = name
                    to_address.save()
                elif main_address.address == address:
                    main_address.name = name
                    main_address.save()
            if Transaction.objects.filter(transaction_hash=item.get('hash', '')).exists():
                # If a transaction already exists, break the loop to stop processing
                break

            transactionCost = calculate_transaction_cost_xrp(
                base_fee_per_gas=int(item.get('base_fee_per_gas', 0)) / 10 ** 9,
                priority_fee_per_gas=2.5,
                total_gas_used=int(item.get('gas_used', 0))
            )

            transaction = Transaction(
                transaction_hash=item.get('hash', ''),
                block_number=item.get('block', 0),
                address=main_address,
                status=item.get('status', ''),
                from_address=from_address,
                to_address=to_address,
                method=item.get('method', ''),
                tx_type=item.get('tx_types', )[0],
                timestamp=parse_datetime(item.get('timestamp')),
                gas_used=int(item.get('gas_used', 0)),
                priority_fee=int(item.get('priority_fee', 0)),
                base_fee_per_gas=int(item.get('base_fee_per_gas', 0)),
                total_gas_paid=transactionCost,
                error_status=item.get('result', ''),
                revert_reason=item.get('revert_reason', '')
            )
            transactions.append(transaction)

            try:
                transaction.save()
            except IntegrityError:
                break

        main_address.last_block_number = transactions[len(transactions) - 1].block_number
        main_address.save()

        return Response(TransactionSerializer(transactions, many=True).data)
    except requests.exceptions.HTTPError as http_err:
        print(http_err)
        return Response({"error": str(http_err)}, status=response.status_code)
    except requests.exceptions.RequestException as err:
        print(err)
        return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_transactions_by_address(request, address):
    """
    API endpoint to retrieve transactions for a given address in a paginated format.
    """
    # Filter transactions by address
    queryset = Transaction.objects.filter(address__address=address).order_by('timestamp')
    if not queryset.exists():
        return Response({'message': 'No transactions found for this address.'}, status=404)

    # Fallback if pagination is not applicable
    serializer = TransactionSerializer(queryset, many=True)

    total_gas_spent = 0
    total_fees = 0
    fees_over_time = {
        'labels': [],
        'datasets': [
            {
                'label': 'Fees over time',
                'backgroundColor': '#111827',
                'data': []
            }
        ]
    }

    for transaction in queryset:
        total_gas_spent += int(transaction.total_gas_paid)
        fees_over_time['labels'].append(transaction.timestamp.strftime('%H:%M'))
        fees_over_time['datasets'][0]['data'].append(transaction.total_gas_paid)

    success = queryset.filter(error_status='success')

    response = {
        'transactions': serializer.data,
        'average_gas_price': total_gas_spent / queryset.count(),
        'average_fee_paid': total_fees / queryset.count(),
        'failed_transactions': queryset.count() - success.count(),
        'succeded_transactions': success.count(),
        'fees_over_time_graph': fees_over_time,
    }

    return Response(response)

@api_view(['GET'])
def fees_over_time(request, address):
    queryset = Transaction.objects.filter(address__address=address).order_by('timestamp')
    if not queryset.exists():
        return Response({'message': 'No transactions found for this address.'}, status=404)

    fees_over_time = {
        'labels': [],
        'datasets': [
            {
                'label': 'Fees over time',
                'backgroundColor': '#111827',
                'data': []
            }
        ]
    }

    for transaction in queryset:
        fees_over_time['labels'].append(transaction.timestamp.strftime('%H:%M'))
        fees_over_time['datasets'][0]['data'].append(transaction.total_gas_paid)

    return Response(fees_over_time)

@api_view(['GET'])
def gas_fee(request, address):
    queryset = Transaction.objects.filter(address__address=address)
    if not queryset.exists():
        return Response({'message': 'No transactions found for this address.'}, status=404)

    # Fallback if pagination is not applicable
    serializer = TransactionSerializer(queryset, many=True)

    total_gas_spent = 0
    total_fees = 0
    for transaction in queryset:
        total_gas_spent += int(transaction.total_gas_paid)

    return Response(total_gas_spent / queryset.count())


def calculate_transaction_cost_xrp(base_fee_per_gas, priority_fee_per_gas, total_gas_used):
    """
    Calculates the total transaction cost in XRP.

    Parameters:
    - base_fee_per_gas (float): The base fee per gas in Gwei.
    - priority_fee_per_gas (float): The priority fee per gas in Gwei.
    - total_gas_used (int): Total gas used in the transaction.

    Returns:
    - float: Total transaction cost in XRP.
    """
    # Calculate the total fee per gas in Gwei
    total_fee_per_gas = base_fee_per_gas + priority_fee_per_gas

    # Convert Gwei to XRP (1 Gwei = 10^-9 ETH/XRP)
    total_fee_per_gas_in_xrp = total_fee_per_gas * 10 ** -9

    # Calculate total transaction cost in XRP
    total_transaction_cost_xrp = total_fee_per_gas_in_xrp * total_gas_used

    return total_transaction_cost_xrp


@api_view(['GET'])
def all_address(request):
    return Response(AddressSerializer(Address.objects.filter(name__isnull=False), many=True).data)
