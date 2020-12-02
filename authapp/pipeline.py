from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from geekshop.settings import BASE_DIR


# def get_api_vk(response, method, *args):
#     print(args)
#     print(len(args))
#     if len(args) > 1:
#         api_url = urlunparse(('https',
#                               'api.vk.com',
#                               '/method/' + method,
#                               None,
#                               urlencode(OrderedDict(fields=','.join(args),
#                                                     access_token=response['access_token'],
#                                                     v='5.124')), None))
#
#     else:
#         api_url = urlunparse(('https',
#                               'api.vk.com',
#                               '/method/' + method,
#                               None,
#                               urlencode(OrderedDict(fields=args[0],
#                                                     access_token=response['access_token'],
#                                                     v='5.124')), None))
#     return api_url


def save_user_profile_vk(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200', 'domain')),
                                                access_token=response['access_token'],
                                                v='5.124')), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if data['photo_200']:
        get_photo = requests.get(data['photo_200'])
        with open(f'{BASE_DIR}/media/users_avatars/{user.id}.jpg', 'wb') as photo:
            photo.write(get_photo.content)
        user.avatar = f'users_avatars/{user.id}.jpg'

    if data['domain']:
        user.shopuserprofile.social_page = f"https://vk.com/{data['domain']}"

    # api_request = get_api_vk(response, 'account.getInfo', 'fields')
    # print(api_request)
    # resp = requests.get(api_request)
    # print(resp)



    # if data_lang['lang']:
    #     user.shopuserprofile.localization = data_lang['lang']

    user.save()


def save_user_profile_google(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    if response['picture']:
        get_photo = requests.get(response['picture'])
        with open(f'{BASE_DIR}/media/users_avatars/{user.id}.jpg', 'wb') as photo:
            photo.write(get_photo.content)
        user.avatar = f'users_avatars/{user.id}.jpg'

    if response['locale']:
        user.shopuserprofile.localization = response['locale']



    for el in response:
        print(el)





