from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import isAuthenticated
from rest_framework.authentication import TokenAuthentication
from caps.pagination import CustomNumberPagination
from services.models import Service
from services.permissions import OwnerOrAdmPermission
from services.serializers import ServiceSerializer
from services.utils.mixins import SerializerByMethodMixin

from users.models import User


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
    


class ServiceRetrieveUpdateDeleteView(SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAuthenticated, OwnerOrAdmPermission]
    queryset =  Service.objects.all()
    serializer_class = ServiceSerializer
