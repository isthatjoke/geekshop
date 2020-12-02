from django.core.cache import cache
from django.db import models

# Create your models here.
from django.utils.functional import cached_property


class GameTypes(models.Model):
    name = models.CharField(verbose_name="name", max_length=64, unique=True)
    description = models.TextField(verbose_name="description", blank=True)
    is_active = models.BooleanField(verbose_name="active", default=True, db_index=True)

    class Meta:
        verbose_name = "type"
        verbose_name_plural = "types"

    def __str__(self):
        return self.name


class Game(models.Model):
    type = models.ForeignKey(GameTypes, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="name", max_length=50)
    image = models.ImageField(upload_to="games_images", blank=True)
    short_desc = models.CharField(verbose_name="short description", max_length=70, blank=True)
    description = models.TextField(verbose_name="description", blank=True)
    price = models.DecimalField(verbose_name="price", max_digits=6, decimal_places=2, default=0)
    quantity = models.SmallIntegerField(verbose_name="quantity at warehouse", default=0)
    is_active = models.BooleanField(verbose_name="active", default=True, db_index=True)

    def __str__(self):
        return f'{self.name} {self.type.name}'

    @staticmethod
    def get_items():
        games = cache.get('all_games')
        if games is None:
            games = Game.objects.filter(is_active=True).order_by('name').select_related()
            cache.set('all_games', games)
        return games


class Router(models.Model):
    specifications = models.FileField(upload_to='router_specifications')


