from django.urls import path

from .views import sync_data, health_check, get_transactions_by_address, all_address, gas_fee

urlpatterns = [
    path('health-check/', health_check),
    path('all/', all_address),
    path('gas-fees/<str:address>/', gas_fee),
    path('sync-data/<str:address>/<str:name>/', sync_data),
    path('sync-data/<str:address>/', sync_data),
    path('<str:address>/', get_transactions_by_address),

]
