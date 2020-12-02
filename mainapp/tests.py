from django.core.management import call_command
from django.test import TestCase, Client


# Create your tests here.
from mainapp.models import GameTypes, Game

SUCCESS_STATUS = 200
BAD_STATUS = 400


class TestMainappTestCase(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')

        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)

        response = self.client.get('/gallery/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)

        response = self.client.get('/services/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)

        for gametype in GameTypes.objects.all():
            response = self.client.get(f'/gallery/{gametype.pk}')
            self.assertEqual(response.status_code, SUCCESS_STATUS)

        for game in Game.objects.all():
            response = self.client.get(f'/gallery/game/{game.pk}')
            self.assertEqual(response.status_code, SUCCESS_STATUS)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'shopping_catrapp')


