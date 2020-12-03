from rest_framework import serializers
from mainapp.models import Game, GameTypes


class GamesSerializer(serializers.ModelSerializer):
    # type = serializers.RelatedField(read_only=True)

    class Meta:
        model = Game
        fields = ('type', 'name', 'short_desc', 'description', 'price', 'quantity')

    # name = serializers.CharField(max_length=50)
    # short_desc = serializers.CharField(max_length=70)
    # description = serializers.CharField(max_length=300)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    # quantity = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)


class GameTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        return GameTypes.objects.create(**validated_data)


# class GamesSerializer(serializers.Serializer):
#     type = serializers.CharField()
#     name = serializers.CharField(max_length=50)
#     short_desc = serializers.CharField(max_length=70)
#     description = serializers.CharField(max_length=300)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
#     quantity = serializers.IntegerField(default=0)
#
#     def create(self, validated_data):
#         return Game.objects.create(**validated_data)