from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='media_folder_games')
def media_folder_games(string):
    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    return f'{settings.MEDIA_URL}{string}'



