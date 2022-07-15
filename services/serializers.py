from rest_framework import serializers
from adresses.models import Address
from adresses.serializers import AddressSerializer

from users.models import User

from .models import Service



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class ServiceSerializer(serializers.ModelSerializer):
    contractor = UserSerializer(read_only=True)
    address = AddressSerializer()
    #category = CategorySerializer()

    class Meta:
        model = Service
        fields = [
            "id",
            "title", 
            "description", 
            "price",  
            "contractor",
            "address"
        ]

    def create(self, validated_data: dict):
        """ 
            Quero gravar o address
            - se não tiver irá pegar no contrante
            - se tiver address tem que verificar se o number e o zipCode
                - se é igual algum address pegar esse id.
                - se não cria outro
                
        """
        address_data = validated_data.pop("address")
        address , check= Address.objects.get_or_create(**address_data) 
        service = Service.objects.create(**validated_data,address=address)
        
   
        return service


