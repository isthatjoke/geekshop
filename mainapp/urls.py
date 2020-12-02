
from django.urls import path
import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    # path('', mainapp.gallery, name='index'),
    path('', mainapp.GamesAllView.as_view(), name='games'),
    path('<int:pk>', mainapp.GamesView.as_view(), name='selected_games'),
    path('game/<int:pk>', mainapp.GameView.as_view(), name='game'),
]
