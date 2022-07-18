from rest_framework import generics
from .models import Address
from .serializers import AddressSerializer
from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User
from utils.permissions import IsOwnerOrReadOnly, IsOwnerOrSuperUserOrReadOnly, IsOwnerAddressOrSuperUserOrReadOnly
import ipdb

class ListCreateAddress(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerAddressOrSuperUserOrReadOnly]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
