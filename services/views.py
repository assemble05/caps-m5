from caps.pagination import CustomNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User

from services.models import Service
from services.permissions import (
    CreateServicePermission,
    GetServiceOwnerOrAdmPermission,
    IsProviderPermission,
    ListContractorServicesPermission,
)
from services.serializers import (
    CandidateToServiceSerializer,
    ListContractorServiceSerializer,
    ListProviderServiceSerializer,
    ServiceSerializer,
    ShowServiceSerializer,
)
from services.utils.mixins import SerializerByMethodMixin


class ServiceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, CreateServicePermission]

    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(contractor=self.request.user)


class ListServiceView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomNumberPagination

    serializer_class = CandidateToServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ListContractorServicesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ListContractorServicesPermission]

    serializer_class = ListContractorServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(contractor=self.request.user)


class ListProviderServicesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ListProviderServiceSerializer

    def get_queryset(self):
        provider = get_object_or_404(User, pk=self.kwargs["provider_id"])
        return Service.objects.filter(provider=provider)


class ServiceRetrieveUpdateDeleteView(
    SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [GetServiceOwnerOrAdmPermission]

    queryset = Service.objects.all()
    serializer_map = {
        "GET": ShowServiceSerializer,
        "PATCH": ServiceSerializer,
        "DELETE": ServiceSerializer,
    }


class CandidateToServiceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsProviderPermission]

    queryset = Service.objects.all()
    serializer_class = CandidateToServiceSerializer

    def perform_update(self, serializer):
        candidate = self.request.user

        service = Service.objects.get(id=self.kwargs["pk"])

        if candidate in service.candidates.all():
            raise KeyError("This user is already a candidate")

        serializer.save(candidate=candidate)
