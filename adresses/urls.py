from django.urls import path
from .views import AddressUserView, ListCreateAddress, AddressDetailView, AddresServiceView




urlpatterns = [
    path('address/', ListCreateAddress.as_view(), name="create_address"),
    path('address/<pk>/', AddressDetailView.as_view(), name="address_detail_view"),
    path("address/services/<pk>/", AddresServiceView.as_view(), name="address_service_view"),
    path("address/users/<pk>/", AddressUserView.as_view(), name="addres_user_view")
]