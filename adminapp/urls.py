
from django.urls import path
import adminapp.views as adminapp


app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.AdminView.as_view(), name='admin'),
    path('users/', adminapp.UserListView.as_view(), name='users'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/edit/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
    path('gametypes/', adminapp.GameTypesView.as_view(), name='game_types'),
    path('gametypes/create/', adminapp.GameTypeCreateView.as_view(), name='game_type_create'),
    path('gametypes/edit/<int:pk>/', adminapp.GameTypeUpdateView.as_view(), name='game_type_update'),
    path('gametypes/delete/<int:pk>/', adminapp.GameTypeDeleteView.as_view(), name='game_type_delete'),
    path('games/gametypes/<int:pk>/', adminapp.GamesView.as_view(), name='games'),
    path('games/create/gametypes/<int:pk>/', adminapp.GameCreateFromTypeView.as_view(), name='game_create_from_type'),
    path('games/create/', adminapp.GameCreateView.as_view(), name='game_create'),
    path('games/edit/<int:pk>/', adminapp.GameUpdateView.as_view(), name='game_update'),
    path('games/delete/<int:pk>/', adminapp.GameDeleteView.as_view(), name='game_delete'),
    path('orders/', adminapp.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', adminapp.OrderUpdateView.as_view(), name='order_update'),
    path('orders/delete/<int:pk>/', adminapp.OrderDeleteView.as_view(), name='order_delete'),
    path('orders/details/<int:pk>', adminapp.OrderDetailUpdateView.as_view(), name='order_details'),
    ]



# path('', adminapp.UserListView.as_view(), name='admin'),
# path('users/', adminapp.users, name='users'),
# path('users/create/', adminapp.user_create, name='user_create'),
# path('users/edit/<int:pk>/', adminapp.user_edit, name='user_edit'),
# path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
# path('gametypes/', adminapp.game_types, name='game_types'),
# path('gametypes/create/', adminapp.game_type_create, name='game_type_create'),
# path('gametypes/edit/<int:pk>/', adminapp.game_type_edit, name='game_type_edit'),
# path('gametypes/delete/<int:pk>/', adminapp.game_type_delete, name='game_type_delete'),
# path('games/create/', adminapp.game_create, name='game_create'),
# path('games/edit/<int:pk>/', adminapp.game_edit, name='game_edit'),
# path('games/delete/<int:pk>/', adminapp.game_delete, name='game_delete'),
# path('games/gametypes/<int:pk>/', adminapp.games, name='games'),
# path('games/create/gametypes/<int:pk>/', adminapp.game_create_from_type, name='game_create_from_type'),
# path('', adminapp.admin, name='admin'),
# path('games/<int:pk>/', adminapp.game, name='game'),