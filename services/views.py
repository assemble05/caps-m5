from django.shortcuts import get_object_or_404
from rest_framework import generics
from services.models import Service
from services.serializers import ServiceSerializer

from users.models import User


# Create your views here.
class ServiceView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer


    def perform_create(self, serializer):
        contractor = get_object_or_404(User, pk=self.kwargs["id_user"])
        serializer.save(contractor=contractor)
    

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["id_user"])
        return Service.objects.filter(contractor=user)
