from django.conf import settings
from django.db import models

# Create your models here.
from mainapp.models import Game


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    DONE = 'DN'
    CANCEL = 'CNL'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'forming'),
        (SENT_TO_PROCEED, 'sent to proceed'),
        (PROCEEDED, 'proceeded'),
        (PAID, 'paid'),
        (READY, 'ready'),
        (DONE, 'done'),
        (CANCEL, 'canceled')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='user')
    created = models.DateTimeField(verbose_name='made', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated', auto_now=True)
    status = models.CharField(verbose_name='status', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    paid = models.DateTimeField(verbose_name='payment_status', auto_now=False, null=True)
    is_active = models.BooleanField(verbose_name='active', default=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Current order: #{self.id}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.game.price, items)))

    def get_summary(self):
        items = self.orderitems.select_related()
        total_cost = sum(list(map(lambda x: x.quantity * x.game.price, items)))
        total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return {
            'total_cost': total_cost,
            'total_quantity': total_quantity,
        }

    def delete(self):
        for item in self.orderitems.select_related():
            item.game.quantity += item.quantity
            item.game.save()

        self.is_active = False
        self.save()

#
# class OrderItemQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.game.quantity += object.quantity
#             object.game.save()
#         super(OrderItemQuerySet, self).delete(*args, **kwargs)


# class OrderItemManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_active=True)


class OrderItem(models.Model):
    # objects = OrderItemQuerySet.as_manager()
    # objects = OrderItemManager()

    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE, verbose_name='order')
    game = models.ForeignKey(Game, verbose_name='game', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='quantity', default=0)

    def get_game_cost(self):
        return self.game.price * self.quantity

    def delete(self):
        self.game.quantity += self.quantity
        self.game.save()

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
