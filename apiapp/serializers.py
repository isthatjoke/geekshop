from rest_framework import serializers


class GamesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    short_desc = serializers.CharField(max_length=70)
    description = serializers.CharField(max_length=300)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = serializers.IntegerField(default=0)
