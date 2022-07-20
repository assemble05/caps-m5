from caps.pagination import CustomNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User

from services.models import Service
from services.permissions import IsProviderPermission, OwnerOrAdmPermission
from services.serializers import CandidateToServiceSerializer, ServiceSerializer
from services.utils.mixins import SerializerByMethodMixin


class ServiceView(generics.CreateAPIView):
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        contractor = get_object_or_404(User, pk=self.kwargs["id_user"])
        serializer.save(contractor=contractor)


class ListServiceView(generics.ListAPIView):
    permission_classes = [OwnerOrAdmPermission]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = CustomNumberPagination


class ServiceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OwnerOrAdmPermission]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


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
