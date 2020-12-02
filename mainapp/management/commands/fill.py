from django.conf import settings
from django.core.management.base import BaseCommand
from mainapp.models import GameTypes, Game
from authapp.models import ShopUser


import json, os


JSON_PATH = 'mainapp/json'


def read_file(filename):
    with open(os.path.join(JSON_PATH, filename + '.json'), 'r') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        types = read_file('gametypes')

        GameTypes.objects.all().delete()
        for type in types:
            new_type = GameTypes(**type)
            new_type.save()

        games = read_file('games')

        Game.objects.all().delete()
        for game in games:
            type_name = game["type"]
            _type = GameTypes.objects.get(name=type_name)
            game['type'] = _type
            new_game = Game(**game)
            new_game.save()

        ShopUser.objects.create_superuser(username='django', password='geekbrains', age=33, email='')
        # CREATE DATABASE "geekshop" ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE template0;