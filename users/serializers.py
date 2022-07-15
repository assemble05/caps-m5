import ipdb
from adresses.models import Address
from adresses.serializers import AddressSerializer
from rest_framework import serializers

from users.models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        fields = [
            "id",
            "password",
            "first_name",
            "last_name",
            "is_provider",
            "description",
            "email",
            "address",
        ]
        model = User
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        address_data = validated_data.pop("address")
        address , check= Address.objects.get_or_create(**address_data) 
        user = User.objects.create_user(**validated_data,address=address)
        
   
        return user


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "is_provider",
            "description",
            "email",
            "address",
            "phone",
        ]
