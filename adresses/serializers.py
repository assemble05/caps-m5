from rest_framework import serializers
from .models import Address
import ipdb

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
    def create(self, validated_data):
        address =  super().create(validated_data)
        user = validated_data.pop("user")
        user.address = address
        user.save()
        return address