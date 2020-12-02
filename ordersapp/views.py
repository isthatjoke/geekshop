from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from datetime import datetime

from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from mainapp.models import Game
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from shopping_cartapp.models import ShoppingCart


class OrderList(ListView):
    model = Order

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related()


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            shopping_cart_items = ShoppingCart.get_items(self.request.user).select_related()
            if len(shopping_cart_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                                     extra=len(shopping_cart_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['game'] = shopping_cart_items[num].game
                    form.initial['quantity'] = shopping_cart_items[num].quantity
                    form.initial['price'] = shopping_cart_items[num].game.price
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            ShoppingCart.get_items(self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.game.price
            data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                if self.object.get_total_cost() == 0:
                    self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderRead(DetailView):
    model = Order

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'order'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.paid = now()
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


def get_game_price(request, pk):
    if request.is_ajax():
        game = Game.objects.filter(pk=int(pk)).first()
        if game:
            return JsonResponse({'price': game.price})
        else:
            return JsonResponse({'price': 0})


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=ShoppingCart)
def game_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.game.quantity = F('quantity') - (instance.quantity - sender.get_item(instance.pk).quantity)
    else:
        instance.game.quantity = F('quantity') - instance.quantity
    instance.game.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=ShoppingCart)
def game_quantity_update_delete(sender, instance, **kwargs):
    instance.game.quantity = F('quantity') + instance.quantity
    instance.game.save()