from django.urls import path
import shopping_cartapp.views as shopping_cartapp


app_name = 'shopping_cartapp'

urlpatterns = [
    path('', shopping_cartapp.shopping_cart, name='shopping_cart'),
    # path('', shopping_cartapp.ShoppingCartListView, name='shopping_cart'),
    path('add/<int:pk>/', shopping_cartapp.add, name='add'), # pk from models.Game
    path('remove/<int:pk>/', shopping_cartapp.remove, name='remove'), # pk from db
    path('edit/<int:pk>/<int:quantity>/', shopping_cartapp.edit, name='edit'),
    ]