from rest_framework import serializers
from users.models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["email", "password","first_name","last_name"]
        model = User
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):

        user = User.objects.create_user(**validated_data)
        return user
