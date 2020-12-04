
from django.urls import path
import apiapp.views as apiapp


app_name = 'apiapp'

urlpatterns = [
    path('games/', apiapp.GamesViewApi.as_view(), name='api_games'),
    path('games/<pk>', apiapp.GamesViewApi.as_view(), name='api_update_game'),
    path('gametypes/', apiapp.GameTypeViewApi.as_view(), name='api_gametypes'),
    path('gametypes/<pk>', apiapp.GameTypeViewApi.as_view(), name='api_update_gametypes'),
]

