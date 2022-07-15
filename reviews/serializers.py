from rest_framework import serializers
from users.models import User

from .models import Review


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class CreateReviewSerializer(serializers.ModelSerializer):
    user_critic = CriticSerializer(read_only=True)
    user_criticized = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "stars", "description"]

    # critic = serializers.SerializerMethodField()
    # criticized = serializers.SerializerMethodField()


#
# def get_critic(self, review: Review):
# return f"{review.user_critic.first_name} {review.user_critic.last_name}"
#
# def get_criticized(self, review: Review):
# return f"{review.user_criticized.first_name} {review.user_criticized.last_name}"
