from rest_framework import serializers
from mainapp.models import Game, GameTypes


class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('pk', 'type', 'name', 'short_desc', 'description', 'price', 'quantity')

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.pk = validated_data.get('pk', instance.pk)
        instance.type = validated_data.get('type', instance.type)
        instance.name = validated_data.get('name', instance.name)
        instance.short_desc = validated_data.get('short_desc', instance.short_desc)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)

        instance.save()
        return instance


class GameTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameTypes
        fields = ('pk', 'name', 'description')

    def create(self, validated_data):
        return GameTypes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.pk = validated_data.get('pk', instance.pk)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance

