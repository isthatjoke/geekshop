from django.conf import settings
from django.db import models

# Create your models here.
from django.utils.functional import cached_property

from mainapp.models import Game


# class ShoppingCartQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.game.quantity += object.quantity
#             object.game.save()
#         super(ShoppingCartQuerySet, self).delete(*args, **kwargs)


class ShoppingCart(models.Model):
    # objects = ShoppingCartQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shopping_cart")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(verbose_name="quantity", default=0)
    add_time = models.DateTimeField(verbose_name="add time", auto_now_add=True)

    @staticmethod
    def get_item(pk):
        return ShoppingCart.objects.get(pk=pk)

    @cached_property
    def get_items_cached(self):
        return self.user.shopping_cart.select_related()

    @staticmethod
    def get_items(user):
        return ShoppingCart.objects.filter(user=user).order_by('game__type').select_related()

    @property
    def product_cost(self):
        return self.game.price * self.quantity

    @property
    def total_quantity(self):
        # _items = ShoppingCart.objects.filter(user=self.user).select_related()
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        # _items = ShoppingCart.objects.filter(user=self.user).select_related()
        _items = self.get_items_cached
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    @staticmethod
    def get_game(user, game):
        return ShoppingCart.objects.filter(user=user, game=game).select_related()

    # def delete(self, *args, **kwargs):
    #     self.game.quantity += self.quantity
    #     self.game.save()


    # def save(self, *args, **kwargs):
    #     self.game.quantity -= 1
    #     self.game.save()
    #     super(ShoppingCart, self).save(*args, **kwargs)

