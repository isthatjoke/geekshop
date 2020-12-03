from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from mainapp.models import Game, GameTypes
from apiapp.serializers import GamesSerializer, GameTypeSerializer


class GamesViewApi(APIView):

    def get(self, request):
        games = Game.objects.filter(is_active=True)
        serializer = GamesSerializer(games, many=True)

        return Response({'games': serializer.data})

    def post(self, request):
        games = request.data.get('games')
        serializer = GamesSerializer(data=games)
        if serializer.is_valid(raise_exception=True):
            games_saved = serializer.save()

        return Response({'success': f'Game {games_saved.name} created successfully'})


class GameTypeViewApi(APIView):

    def get(self, request):
        gametypes = GameTypes.objects.filter(is_active=True)
        serializer = GameTypeSerializer(gametypes, many=True)

        return Response({'gametypes': serializer.data})

    def post(self, request):
        gametypes = request.data.get('gametypes')
        serializer = GameTypeSerializer(data=gametypes)
        if serializer.is_valid(raise_exception=True):
            gametypes_saved = serializer.save()

        return Response({'success': f'Gametype {gametypes_saved.name} created successfully'})

