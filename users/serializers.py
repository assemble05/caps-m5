import ipdb
from adresses.models import Address
from adresses.serializers import AddressSerializer
from rest_framework import serializers

from users.models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

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
        read_only_fields = ["address"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        try:
            address_data = validated_data.pop("address")
            address , check= Address.objects.get_or_create(**address_data) 
            user = User.objects.create_user(address=address,**validated_data)
            return user
        except:
            user = User.objects.create_user(**validated_data)
            return user
   
        # return user

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        
        instance.save()

        return instance

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "is_provider",
            "description",
            "email",
            "address",
            "phone",
        ]

class UserProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "is_provider",
            "description",
            "email",
            "address",
            "phone",
            "critics",
        ]
    

    