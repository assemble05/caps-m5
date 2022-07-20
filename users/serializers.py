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
        fields = ["nome", "description"]


class UserRegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    categories = serializers.SerializerMethodField()
    categories_id = serializers.ListField(write_only=True, required=False)

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
            "categories",
            "categories_id",
        ]
        model = User
        read_only_fields = ["categories"]
        extra_kwargs = {
            "password": {"write_only": True},
            "categories_id": {"write_only": True},
        }

    def get_categories(self, obj: User):
        return CatSerializer(obj.categories.all(), many=True).data

    def create(self, validated_data: dict):

        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)

        if "categories_id" in validated_data.keys():
            categories_data = validated_data.pop("categories_id")
            user = User.objects.create_user(address=address, **validated_data)
            user.categories.set(categories_data)
            return user

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
    critics = serializers.SerializerMethodField()
    address = AddressSerializer()
    review_score = serializers.SerializerMethodField()

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
            "review_score"
        ]
    
    def get_review_score(self, obj):
        total = 0
        if obj.critics.count() == 0:
            return None
        for star in obj.critics.all():
            total += star.stars
        return total/obj.critics.count()
    
    def get_critics(self, obj):
        return obj.critics.count()
