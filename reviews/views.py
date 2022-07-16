from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from services.models import Service
from users.models import User

from .mixins import SerializerByMethodMixin
from .models import Review
from .permissions import OwnerOrAdmPermission
from .serializers import ReviewSerializer, UpdateReviewSerializer


# Create your views here.
class ReviewView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        user_criticized = get_object_or_404(User, pk=self.kwargs["id_user"])
        serializer.save(user_critic=self.request.user, user_criticized=user_criticized)

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["id_user"])
        return Review.objects.filter(user_criticized=user)


class CreateReviewView(generics.CreateAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        service = get_object_or_404(Service, pk=self.kwargs["id_service"])
        if self.request.user.is_provider:
            user_critic = service.contractor
            serializer.save(
                user_critic=user_critic,
                user_criticized=self.request.user,
                service=service,
            )
        else:
            user_criticized = service.provider
            serializer.save(
                user_critic=self.request.user,
                user_criticized=user_criticized,
                service=service,
            )


class ReviewParamsView(SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [OwnerOrAdmPermission]

    queryset = Review.objects.all()
    serializer_map = {
        "GET": ReviewSerializer,
        "DELETE": ReviewSerializer,
        "PATCH": UpdateReviewSerializer,
    }

    lookup_url_kwarg = "id_user"
