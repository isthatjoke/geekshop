import json
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from mainapp.models import Game
from shopping_cartapp.models import ShoppingCart


JSON_DIR = os.path.join(settings.BASE_DIR, 'mainapp/json')
with open(os.path.join(JSON_DIR, 'links_menu.json'), 'r') as file:
    temp_data = json.load(file)
    links_menu = temp_data["links"]

#
# class ShoppingCartListView(ListView):
#     model = ShoppingCart
#     template_name = 'shopping_cartapp/shopping_cart.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'shopping cart'
#         context['links_menu'] = links_menu
#         return context
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = super(ShoppingCartListView, self).get_queryset(*args, **kwargs)
#         print(queryset)
#         return ShoppingCart.objects.get(user=self.request.user)


@login_required()
def shopping_cart(request):
    title = 'shopping cart'
    DOMAIN = settings.DOMAIN_NAME
    shopping_cart_items = ShoppingCart.objects.filter(user=request.user).select_related()
    content = {
        'links_menu': links_menu,
        'title': title,
        'shopping_cart_items': shopping_cart_items,
        'domain': DOMAIN,
    }
    return render(request, 'shopping_cartapp/shopping_cart.html', content)


@login_required()
def add(request, pk=None):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('gallery:game', args=[pk]))

    game = get_object_or_404(Game, pk=pk)
    old_shopping_cart = ShoppingCart.get_game(user=request.user, game=game)

    if old_shopping_cart:
        old_shopping_cart[0].quantity = F('quantity') + 1
        old_shopping_cart[0].save()
    else:
        new_shopping_cart = ShoppingCart(user=request.user, game=game)
        new_shopping_cart.quantity += 1
        new_shopping_cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def remove(request, pk=None):
    shopping_cart_remove = get_object_or_404(ShoppingCart, pk=pk)
    shopping_cart_remove.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_shopping_cart_item = ShoppingCart.objects.get(pk=int(pk))

        if quantity > 0:
            new_shopping_cart_item.quantity = quantity
            new_shopping_cart_item.save()

        else:
            new_shopping_cart_item.delete()

        shopping_cart_items = ShoppingCart.objects.filter(user=request.user).select_related()

        content = {
            'shopping_cart_items': shopping_cart_items,
        }

        result = render_to_string('shopping_cartapp/includes/inc_shopping_cart_list.html', content)

        return JsonResponse({'result': result})
