from rest_framework import serializers


class IngredientsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256, source='name')
    dimension = serializers.CharField(max_length=16, source='unit')
