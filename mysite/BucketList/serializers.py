from rest_framework import serializers
from .models import Bucket

class BucketlistSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Bucket
        fields = ('id', 'name')
