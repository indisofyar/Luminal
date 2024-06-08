from django.urls import path

from .views import hello_world, get_data

urlpatterns = [
    path('hello-world/', hello_world),
    path('get-data/<str:address>/', get_data),
]
