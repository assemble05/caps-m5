from rest_framework import serializers
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["id", "nome", "description", "services", "users"]

    services = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_services(self, category: Category):
        return category.services.count()

    def get_users(self, category: Category):
        return category.providers.count()

    def create(self, validated_data: dict):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):

        if 'providers' in validated_data:
            raise KeyError('You can not update providers property.')

        instance.nome = validated_data.get('nome', instance.nome)
        instance.description = validated_data.get('description', instance.description)
        
        instance.save()

        return instance
