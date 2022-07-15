from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User

from .models import Review
from .serializers import CreateReviewSerializer


# Create your views here.
class ReviewView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer

    def perform_create(self, serializer):
        user_criticized = get_object_or_404(User, pk=self.kwargs["id_user"])
        serializer.save(user_critic=self.request.user, user_criticized=user_criticized)
