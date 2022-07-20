import ipdb
from pkg_resources import require
from adresses.models import Address
from adresses.serializers import AddressSerializer
from rest_framework import serializers
from reviews.models import Review
from categories.models import Category
from users.models import User
from categories.serializers import CategorySerializer


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
class UserRegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    # categories = CatSerializer(allow_null=True, required=False)
    class Meta:
        fields = [
            "id",
            "password",
            "first_name",
            "last_name",
            "is_provider",
            "description",
            "email",
            "address"
        ]
        model = User
        read_only_fields = ["address","categories"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):

        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        user = User.objects.create_user(address=address, **validated_data)


        return user

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()

        return instance


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "stars",
            "description",
        ]


class UserSerializer(serializers.ModelSerializer):
    critics = ReviewUserSerializer(many=True)
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
            "critics",
        ]
