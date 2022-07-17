from django.shortcuts import get_object_or_404
from rest_framework import generics
from services.models import Service
from .serializers import DocumentsSeriarializer

from users.models import User


# Create your views here.
class DocumentsView(generics.ListCreateAPIView):
    serializer_class = DocumentsSeriarializer


    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs["id_user"])
        serializer.save(user=user)
    

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["id_user"])
        return Service.objects.filter(user=user)
