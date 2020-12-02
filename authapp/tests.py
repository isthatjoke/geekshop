from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, Client


# Create your tests here.
from authapp.models import ShopUser

SUCCESS_STATUS = 200
REDIRECT_STATUS = 302
BAD_STATUS = 400


class TestAuthappTestCase(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')

        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser('su_user', 'su_test@mail.test', 'su_password')
        self.user = ShopUser.objects.create_user('user', 'test@mail.test', 'password')
        self.user_with__first_name = ShopUser.objects.create_user('wn_user', 'wn_test@mail.test', 'wn_password',
                                                                  first_name='username')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'GAME-WORLD')

        self.client.login(username='user', password='password')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.context['user'], self.user)

        response = self.client.get('/')
        self.assertEqual(response.context['user'], self.user)

    def test_user_logout(self):
        self.client.login(username='user', password='password')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, REDIRECT_STATUS)

        response = self.client.get('/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)
        self.assertEqual(response.context['title'], 'register')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'test_user',
            'first_name': 'Johnny',
            'password1': 'country1Q',
            'password2': 'country1Q',
            'email': 'johnny@mail.test',
            'age': '33'
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, REDIRECT_STATUS)

        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, SUCCESS_STATUS)

        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=SUCCESS_STATUS)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'test_user2',
            'first_name': 'johnny2',
            'last_name': 'cash2',
            'password1': 'country2',
            'password2': 'country2',
            'email': 'johnny2@mail.test',
            'age': '17'
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, SUCCESS_STATUS)
        self.assertFormError(response, 'register_form', 'age', "Dude! you're too young!")

    def test_shopping_cart_login_redirect(self):
        response = self.client.get('/shopping_cart/')
        self.assertEqual(response.url, '/auth/login/?next=/shopping_cart/')
        self.assertEqual(response.status_code, REDIRECT_STATUS)

        self.client.login(username='user', password='password')
        response = self.client.get('/shopping_cart/')
        self.assertEqual(response.status_code, SUCCESS_STATUS)
        self.assertEqual(list(response.context['shopping_cart']), [])
        self.assertEqual(response.request['PATH_INFO'], '/shopping_cart/')


    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'shopping_catrapp')