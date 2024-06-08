from django.urls import path

from .views import sync_data, health_check

urlpatterns = [
    path('health-check/', health_check),
    path('sync-data/<str:address>/<str:name>/', sync_data),
    path('sync-data/<str:address>/', sync_data),
]
