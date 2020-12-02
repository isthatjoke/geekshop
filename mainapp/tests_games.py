from django.test import TestCase
from mainapp.models import GameTypes, Game


class TestGamesTestCase(TestCase):
    def setUp(self):
        game_type = GameTypes.objects.create(name='sexual_games')
        self.game_1 = Game.objects.create(name='new_1', type=game_type, price=10, quantity=2)
        self.game_2 = Game.objects.create(name='new_2', type=game_type, price=15, quantity=3, is_active=False)
        self.game_3 = Game.objects.create(name='new_3', type=game_type, price=20, quantity=4)

    def test_game_get(self):
        game_1 = Game.objects.get(name='new_1')
        game_2 = Game.objects.get(name='new_2')
        self.assertEqual(game_1, self.game_1)
        self.assertEqual(game_2, self.game_2)

    def test_game_print(self):
        game_1 = Game.objects.get(name='new_1')
        game_2 = Game.objects.get(name='new_2')
        self.assertEqual(str(game_1), 'new_1 sexual_games')
        self.assertEqual(str(game_2), 'new_2 sexual_games')

    def test_game_get_item(self):
        game_1 = Game.objects.get(name='new_1')
        game_3 = Game.objects.get(name='new_3')
        games = game_1.get_items()

        self.assertEqual(list(games), [game_1, game_3])