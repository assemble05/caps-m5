from django.shortcuts import get_object_or_404
from rest_framework import generics
from services.models import Service

from users.models import User


# Create your views here.
class ServiceView(generics.ListCreateAPIView):

    def perform_create(self, serializer):
        user_criticized = get_object_or_404(User, pk=self.kwargs["id_user"])
        serializer.save(contractor=self.request.user, contractor=user_criticized)

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["id_user"])
        return Service.objects.filter(contractor=user)
