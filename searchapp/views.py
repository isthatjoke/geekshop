import json
import os

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView

from mainapp.models import Game

JSON_DIR = os.path.join(settings.BASE_DIR, 'mainapp/json')
with open(os.path.join(JSON_DIR, 'links_menu.json'), 'r') as file:
    temp_data = json.load(file)
    links_menu = temp_data["links"]





class SearchView(ListView):
    model = Game
    template_name = 'searchapp/search.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'search'
        context['links_menu'] = links_menu
        return context

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            games = Game.objects.filter(name__icontains=search_query).order_by('name')
            return games
        return Game.objects.filter(is_active=True)
