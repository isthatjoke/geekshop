
from django.urls import path
import apiapp.views as apiapp


app_name = 'apiapp'

urlpatterns = [
    path('games/', apiapp.GamesViewApi.as_view(), name='api_games')
]

