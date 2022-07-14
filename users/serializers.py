from rest_framework import serializers
from users.models import User
from adresses.models import Address 
from adresses.serializers import AddressSerializer
import ipdb


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        fields = ["password","first_name","last_name","is_provider","description","phone","email","address"]
        model = User
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        address_data = validated_data.pop("address")
        address , _= Address.objects.get_or_create(**address_data)
        ipdb.set_trace()
        user = User.objects.create_user(**validated_data,address=address)
        
   
        return user
