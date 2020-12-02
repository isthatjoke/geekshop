from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from mainapp.models import Game
from apiapp.serializers import GamesSerializer


class GamesViewApi(APIView):

    def get(self, request):
        games = Game.objects.filter(is_active=True)
        serializer = GamesSerializer(games, many=True)
        return Response({'games': serializer.data})


