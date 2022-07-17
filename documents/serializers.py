from rest_framework import serializers

from services.serializers import UserSerializer
from .models import Documents

class DocumentsSeriarializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Documents
        fields = "__all__"