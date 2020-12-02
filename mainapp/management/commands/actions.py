from datetime import timedelta

from django.core.management import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        SALE_1 = 1
        SALE_2 = 2
        SALE_EXPIRED = 3

        sale_1__time_delta = timedelta(hours=12)
        sale_2__time_delta = timedelta(days=1)

        sale_1__discount = 0.3
        sale_2__discount = 0.15
        sale_expired__discount = 0.05

        sale_1__condition = Q(order__updated__lte=F('order__created') + sale_1__time_delta)
        sale_2__condition = Q(order__updated__gt=F('order__created') + sale_1__time_delta) & \
                            Q(order__updated__lte=F('order__created') + sale_2__time_delta)
        sale_expired__condition = Q(order__updated__gt=F('order__created') + sale_2__time_delta)

        sale_1__order = When(sale_1__condition, then=SALE_1)
        sale_2__order = When(sale_2__condition, then=SALE_2)
        sale_expired__order = When(sale_expired__condition, then=SALE_EXPIRED)

        sale_1__price = When(sale_1__condition, then=F('game__price') * F('quantity') * sale_1__discount)
        sale_2__price = When(sale_2__condition, then=F('game__price') * F('quantity') * sale_2__discount)
        sale_expired_price = When(sale_expired__condition, then=F('game__price') * F('quantity') * sale_expired__discount)

        test_orders = OrderItem.objects.annotate(
            sale_order=Case(
                sale_1__order,
                sale_2__order,
                sale_expired__order,
                output_field=IntegerField(),
            )
        ).annotate(
            total_price=Case(
                sale_1__price,
                sale_2__price,
                sale_expired_price,
                output_field=DecimalField(),
            )
        ).order_by('sale_order', 'total_price').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.sale_order:2}: заказ №{orderitem.pk:3}:\
                   {orderitem.game.name:15}: скидка\
                   {abs(orderitem.total_price):6.2f} руб. | \
                   {orderitem.order.updated - orderitem.order.created}')

