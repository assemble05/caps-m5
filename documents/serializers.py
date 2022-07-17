from rest_framework import serializers
from .models import Documents

class DocumentsSeriarializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"