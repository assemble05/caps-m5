from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from services.models import Service
from users.models import User

from .models import Review
from .permissions import IsInTheServicePermission, OwnerOrAdmPermission
from .serializers import ReviewSerializer


# Create your views here.
class ListCreatedReviewView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["id_user"])
        return Review.objects.filter(user_critic=user)


class ListReceivedReviewView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["id_user"])
        return Review.objects.filter(user_criticized=user)


class CreateReviewView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsInTheServicePermission]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):

        service = get_object_or_404(Service, pk=self.kwargs["id_service"])
        if self.request.user.is_provider:
            user_criticized = service.contractor
            serializer.save(
                user_critic=self.request.user,
                user_criticized=user_criticized,
                service=service,
            )
        else:
            user_criticized = service.provider
            serializer.save(
                user_critic=self.request.user,
                user_criticized=user_criticized,
                service=service,
            )


class ReviewParamsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [OwnerOrAdmPermission]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    lookup_url_kwarg = "id_user"
