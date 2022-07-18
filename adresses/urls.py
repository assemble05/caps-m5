from django.urls import path
from .views import ListCreateAddress, AddressDetailView




urlpatterns = [
    path('address/', ListCreateAddress.as_view(), name="create_address"),
    path('address/<pk>/', AddressDetailView.as_view(), name="address_detail_view"),
]