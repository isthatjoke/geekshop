from shopping_cartapp.models import ShoppingCart


def shopping_cart(request):
    shopping_cart = []

    if request.user.is_authenticated:
        # shopping_cart = ShoppingCart.objects.filter(user=request.user).select_related()
        shopping_cart = request.user.shopping_cart.select_related()

    return {
        'shopping_cart':
            shopping_cart,
    }