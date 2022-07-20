from adresses.models import Address
from adresses.serializers import AddressSerializer
from categories.models import Category
from rest_framework import serializers
from users.models import User

from .models import Service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "nome"]
        read_only_fields = ["nome"]


class ServiceSerializer(serializers.ModelSerializer):
    contractor = UserSerializer(read_only=True)
    address = AddressSerializer(required=False)
    category_id = serializers.UUIDField(write_only=True)
    provider_id = serializers.UUIDField(write_only=True, required=False)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "category",
            "description",
            "price",
            "contractor",
            "provider",
            "address",
            "category_id",
            "provider_id",
        ]

    provider = serializers.SerializerMethodField()

    def get_provider(self, service: Service):

        if service.provider:
            return UserSerializer(instance=service.provider).data

        return None

    def create(self, validated_data: dict):

        category = Category.objects.get(id=validated_data["category_id"])
        if "address" in validated_data.keys():
            address_data = validated_data.pop("address")
            try:
                address = Address.objects.get(
                    zip_code=address_data["zip_code"], number=address_data["number"]
                )
                service = Service.objects.create(
                    address=address, category=category, **validated_data
                )
                return service
            except:
                address = Address.objects.create(**address_data)
                service = Service.objects.create(
                    address=address, category=category, **validated_data
                )
                return service

        address = Address.objects.get(id=validated_data["contractor"].address.id)
        service = Service.objects.create(
            address=address, category=category, **validated_data
        )

        return service

    def update(self, instance, validated_data):
        if "address" in validated_data.keys():
            address_data = validated_data.pop("address")
            try:
                address = Address.objects.get(
                    zip_code=address_data["zip_code"], number=address_data["number"]
                )
                instance.address = address
                instance.save()
            except:
                address = Address.objects.create(**address_data)
                instance.address = address
                instance.save()

        if "category_id" in validated_data.keys():
            category_id = validated_data.pop("category_id")
            category = Category.objects.get(id=category_id)

            instance.category = category
            instance.save()

        if "provider_id" in validated_data.keys():
            provider_id = validated_data.pop("provider_id")
            provider = User.objects.get(id=provider_id)

            instance.provider = provider
            instance.is_active = False
            instance.save()

        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance


class CandidateToServiceSerializer(serializers.ModelSerializer):
    contractor = UserSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "category",
            "description",
            "price",
            "contractor",
            "address",
            "candidates",
        ]

    candidates = serializers.SerializerMethodField()

    def get_candidates(self, service: Service):
        # UserSerializer(service.candidates.all(), many=True).data
        return service.candidates.count()

    def update(self, instance, validated_data):
        candidate = validated_data.pop("candidate")

        instance.candidates.add(candidate)
        instance.save()
        return instance


class ListContractorServiceSerializer(serializers.ModelSerializer):
    contractor = UserSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "category",
            "description",
            "price",
            "contractor",
            "provider",
            "address",
            "candidates",
        ]

    candidates = serializers.SerializerMethodField()

    def get_candidates(self, service: Service):
        return service.candidates.count()

    provider = serializers.SerializerMethodField()

    def get_provider(self, service: Service):

        if service.provider:
            return UserSerializer(instance=service.provider).data

        return None


class ListProviderServiceSerializer(serializers.ModelSerializer):
    contractor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "category",
            "description",
            "contractor",
            "provider",
        ]

    provider = serializers.SerializerMethodField()

    def get_provider(self, service: Service):

        if service.provider:
            return UserSerializer(instance=service.provider).data

        return None


class ShowServiceSerializer(serializers.ModelSerializer):
    contractor = UserSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "category",
            "description",
            "price",
            "contractor",
            "provider",
            "address",
            "candidates",
        ]

    candidates = serializers.SerializerMethodField()

    def get_candidates(self, service: Service):

        if (
            self._context["request"].user == service.contractor
            or self._context["request"].user.is_superuser
        ):
            return UserSerializer(service.candidates.all(), many=True).data

        return service.candidates.count()

    provider = serializers.SerializerMethodField()

    def get_provider(self, service: Service):

        if service.provider:
            return UserSerializer(instance=service.provider).data

        return None
