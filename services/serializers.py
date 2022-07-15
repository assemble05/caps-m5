from rest_framework import serializers
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
    adresses = AddressSerializer()
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

    # def create(self, instance, validated_data):
        """ 
            Quero gravar o address
            - se não tiver irá pegar no contrante
            - se tiver address tem que verificar se o number e o zipCode
                - se é igual algum address pegar esse id.
                - se não cria outro
                
        """
    #    if not validated_data.adresses:
    #       ...


