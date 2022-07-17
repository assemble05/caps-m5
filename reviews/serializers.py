from rest_framework import serializers
from services.models import Service
from users.models import User

from .models import Review


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "price", "category"]
        read_only_fields = ["title", "price", "category"]


class ReviewSerializer(serializers.ModelSerializer):
    user_critic = CriticSerializer(read_only=True)
    user_criticized = CriticSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "description",
            "user_critic",
            "user_criticized",
            "service",
        ]
