from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from adminapp.forms import GameTypeEditForm, GameEditForm, ShopUserAdminEditForm, OrderEditForm, OrderItemEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import GameTypes, Game
from ordersapp.models import Order, OrderItem


@receiver(pre_save, sender=GameTypes)
def update_is_active_from_type_to_game(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.game_set.update(is_active=True)
        else:
            instance.game_set.update(is_active=False)


class AdminView(TemplateView):
    template_name = 'adminapp/admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'admin'
        return context


class UserListView(ListView):
    queryset = ShopUser.objects.all().order_by('-is_active')
    template_name = 'adminapp/users.html'
    # ordering = ['-is_active']
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'users'
        return context


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_edit.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'create user'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_edit.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'update user'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete user'
        return context

    def get_template_names(self):
        names = super().get_template_names()
        return names

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class GameTypesView(ListView):
    model = GameTypes
    template_name = 'adminapp/game_types.html'
    ordering = ['-is_active']

    @method_decorator(user_passes_test((lambda u: u.is_superuser)))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'game types'
        return context


class GameTypeCreateView(CreateView):
    model = GameTypes
    template_name = 'adminapp/game_type_edit.html'
    success_url = reverse_lazy('admin:game_types')
    form_class = GameTypeEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'create game type'
        return context


class GameTypeUpdateView(UpdateView):
    model = GameTypes
    template_name = 'adminapp/game_type_edit.html'
    success_url = reverse_lazy('admin:game_types')
    form_class = GameTypeEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'update game type'
        return context
    
    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.game_set.update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)


class GameTypeDeleteView(DeleteView):
    model = GameTypes
    template_name = 'adminapp/game_type_delete.html'
    success_url = reverse_lazy('admin:game_types')


    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete game type'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class GamesView(ListView):
    model = Game
    template_name = 'adminapp/games.html'
    ordering = ['-is_active']

    @method_decorator(user_passes_test((lambda u: u.is_superuser)))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'games'
        return context

    def game_type(self):
        game_type = self.kwargs.get('pk', None)
        return game_type

    def get_queryset(self):
        type = self.kwargs.get('pk', None)
        if type is not None:
            games = Game.objects.filter(type_id=type).select_related()
            return games
        return Game.objects.all()


class GameCreateFromTypeView(CreateView):
    model = Game
    template_name = 'adminapp/game_edit.html'
    success_url = reverse_lazy('admin:game_types')
    form_class = GameEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.kwargs.get('pk', None)
        context['title'] = 'game create'
        context['form']['type'].initial = type
        return context


class GameCreateView(CreateView):
    model = Game
    template_name = 'adminapp/game_edit.html'
    success_url = reverse_lazy('admin:game_types')
    form_class = GameEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'game create'
        # context['form']['type'].initial = 4
        # print(context['form']['type'])
        # print(context)
        return context


class GameUpdateView(UpdateView):
    model = Game
    template_name = 'adminapp/game_edit.html'
    success_url = reverse_lazy('admin:game_types')
    form_class = GameEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'game update'
        return context


class GameDeleteView(DeleteView):
    model = Game
    template_name = 'adminapp/game_delete.html'
    success_url = reverse_lazy('admin:game_types')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete game'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class OrderListView(ListView):
    queryset = Order.objects.all().order_by('-is_active')
    template_name = 'adminapp/orders.html'
    # ordering = ['-is_active']
    paginate_by = 5

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'orders'
        return context


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'adminapp/order_edit.html'
    success_url = reverse_lazy('admin:orders')
    form_class = OrderEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'update order'
        return context


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'adminapp/order_delete.html'
    success_url = reverse_lazy('admin:orders')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete order'
        return context

    def get_template_names(self):
        names = super().get_template_names()
        return names

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class OrderDetailUpdateView(UpdateView):
    model = OrderItem
    template_name = 'adminapp/order_details.html'
    success_url = reverse_lazy('admin:orders')
    form_class = OrderItemEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'update order details'
        return context










"""
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'users'
    all_users = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    content = {
        'title': title,
        'all_users': all_users,
    }
    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'new user create'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'update_form': user_form,
    }
    return render(request, 'adminapp/user_edit.html', content)
    
    
@user_passes_test(lambda u: u.is_superuser)
def user_edit(request, pk):
    title = 'user edit'
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_edit', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/user_edit.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'user delete'
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))
    content = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def game_types(request):
    title = 'game types'
    _game_types = GameTypes.objects.all().order_by('-is_active')
    content = {
        'title': title,
        'game_types': _game_types,
    }
    return render(request, 'adminapp/game_types.html', content)


@user_passes_test(lambda u: u.is_superuser)
def game_type_create(request):
    title = 'game type create'
    if request.method == 'POST':
        edit_form = GameTypeEditForm(request.POST, request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:game_types'))
    else:
        edit_form = GameTypeEditForm()

    content = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/game_type_edit.html', content)
    
    
    @user_passes_test(lambda u: u.is_superuser)
def game_type_edit(request, pk):
    title = 'game type edit'
    game_type_edit = get_object_or_404(GameTypes, pk=pk)
    if request.method == 'POST':
        edit_form = GameTypeEditForm(request.POST, request.FILES, instance=game_type_edit)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:game_type_edit', args=[game_type_edit.pk]))
    else:
        edit_form = GameTypeEditForm(instance=game_type_edit)

    content = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/game_type_edit.html', content)
    
    
@user_passes_test(lambda u: u.is_superuser)
def game_type_delete(request, pk):
    title = 'game type delete'
    game_type = get_object_or_404(GameTypes, pk=pk)
    if request.method == 'POST':
        game_type.is_active = False
        game_type.save()
        return HttpResponseRedirect(reverse('admin:game_types'))
    content = {
        'title': title,
        'game_type_to_delete': game_type,
    }

    return render(request, 'adminapp/game_type_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def game_create(request):
    title = 'game create'
    if request.method == 'POST':
        edit_form = GameEditForm(request.POST, request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        edit_form = GameEditForm()

    content = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/game_edit.html', content)


@user_passes_test(lambda u: u.is_superuser)
def game_edit(request, pk):
    title = 'game edit'
    game_edit = get_object_or_404(Game, pk=pk)
    game_type = GameTypes.objects.filter(name=game_edit.type).first()
    _game_type = game_type.id
    if request.method == 'POST':
        edit_form = GameEditForm(request.POST, request.FILES, instance='game_edit')
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:game_edit', args=[game_edit.pk]))
    else:
        edit_form = GameEditForm(instance=game_edit)

    content = {
        'title': title,
        'update_form': edit_form,
        'game_type': _game_type,
    }
    return render(request, 'adminapp/game_edit.html', content)


    

@user_passes_test(lambda u: u.is_superuser)
def game_delete(request, pk):
    title = 'game delete'
    game = get_object_or_404(Game, pk=pk)
    game_type = GameTypes.objects.filter(name=game.type).first()
    _game_type = game_type.id
    if request.method == 'POST':
        game.is_active = False
        game.save()
        return HttpResponseRedirect(reverse('admin:game_edit', args=[game.pk]))
    content = {
        'title': title,
        'game_to_delete': game,
        'game_type': _game_type,
    }

    return render(request, 'adminapp/game_delete.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def games(request, pk):
#     title = 'games'
#     game_type = get_object_or_404(GameTypes, pk=pk)
#     _games = Game.objects.filter(type__pk=pk).order_by('-is_active')
#     content = {
#         'title': title,
#         'games': _games,
#         'game_type': game_type,
#     }
#     return render(request, 'adminapp/games.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def game_create_from_type(request, pk):
#     title = 'game create'
#     game_type = get_object_or_404(GameTypes, pk=pk)
#     print(game_type.id)
#     if request.method == 'POST':
#         edit_form = GameEditForm(request.POST, request.FILES, initial={'type': game_type.id})
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:game_edit'))
#     else:
#         edit_form = GameEditForm(initial={'type': game_type.id})
#
#     content = {
#         'title': title,
#         'update_form': edit_form,
#         'game_type': game_type.id
#     }
#     return render(request, 'adminapp/game_edit.html', content)


@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    title = 'admin'

    content = {
        'title': title,

    }
    return render(request, 'adminapp/admin.html', content)



@user_passes_test(lambda u: u.is_superuser)
def game(request, pk):
    title = 'game'
    _game = Game.objects.filter(pk=pk)
    content = {
        'title': title,
        'game': _game,
    }
    return render(request, 'adminapp/game.html', content)
"""