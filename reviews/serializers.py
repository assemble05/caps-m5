from rest_framework import serializers
from users.models import User

from .models import Review


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    user_critic = CriticSerializer(read_only=True)
    user_criticized = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "stars", "description", "user_critic", "user_criticized"]


class UpdateReviewSerializer(serializers.ModelSerializer):
    user_critic = CriticSerializer(read_only=True)
    user_criticized = CriticSerializer(read_only=True)
    user_criticized_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "description",
            "user_critic",
            "user_criticized_id",
            "user_criticized",
        ]

    def update(self, instance, validated_data):

        if "user_criticized_id" in validated_data.keys():
            user_criticized_id = validated_data.pop("user_criticized_id")
            instance.user_criticized = User.objects.get(id=user_criticized_id)
            instance.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()

        return instance
