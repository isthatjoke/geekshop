from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from mainapp.models import Game, GameTypes
from apiapp.serializers import GamesSerializer, GameTypeSerializer



class GamesViewApi(APIView):

    def get(self, request):
        games = Game.objects.all()
        serializer = GamesSerializer(games, many=True)

        return Response({'games': serializer.data})

    def post(self, request):
        games = request.data.get('games')
        serializer = GamesSerializer(data=games)
        if serializer.is_valid(raise_exception=True):
            games_saved = serializer.save()

        return Response({'success': f'Game {games_saved.name} created successfully'})

    def put(self, request, pk):
        games_saved = get_object_or_404(Game.objects.all(), pk=pk)
        data = request.data.get('games')
        serializer = GamesSerializer(instance=games_saved, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            games_saved = serializer.save()

        return Response({"success": f"game {games_saved.name} updated successfully"})

    def delete(self, request, pk):
        game = get_object_or_404(Game.objects.all(), pk=pk)
        game.delete()

        return Response({"message": f"game with id {pk} has been deleted"}, status=204)


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

    def put(self, request, pk):
        gametype_saved = get_object_or_404(GameTypes.objects.all(), pk=pk)
        data = request.data.get('gametypes')
        serializer = GameTypeSerializer(instance=gametype_saved, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            gametype_saved = serializer.save()

        return Response({"success": f"gametype {gametype_saved.name} updated successfully"})

    def delete(self, request, pk):
        game = get_object_or_404(GameTypes.objects.all(), pk=pk)
        game.delete()

        return Response({"message": f"gametype with id {pk} has been deleted"}, status=204)

