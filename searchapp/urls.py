from django.urls import path

import searchapp.views as searchapp

app_name = 'searchapp'

urlpatterns = [
    path('', searchapp.SearchView.as_view(), name='search'),
    # path('', searchapp.search, name='search'),
]