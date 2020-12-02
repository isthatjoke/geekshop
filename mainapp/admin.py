from django.contrib import admin

# Register your models here.
from mainapp.models import GameTypes, Game, Router

admin.site.register(GameTypes)
admin.site.register(Game)
admin.site.register(Router)
