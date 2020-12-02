"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.views.decorators.cache import cache_page

from django.urls import path, include
import mainapp.views as mainapp
from django.conf.urls.static import static



urlpatterns = [
    path('', mainapp.MainView.as_view(), name='main'),
    path('gallery/', include('mainapp.urls', namespace='gallery')),
    path('contacts/', mainapp.ContactsView.as_view(), name='contacts'),
    # path('good/', mainapp.good, name='good'),
    path('about/', mainapp.AboutView.as_view(), name='about'),
    path('services/', mainapp.ServicesView.as_view(), name='services'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('shopping_cart/', include('shopping_cartapp.urls', namespace='shopping_cart')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='order')),
    path('search/', include('searchapp.urls', namespace='search')),
    path('api/', include('apiapp.urls', namespace='api'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     import debug_toolbar
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]



    # path('', mainapp.main, name='main'),
    # path('contacts/',mainapp.contacts, name='contacts'),
    # path('about/', mainapp.about, name='about'),
    # path('services/', mainapp.services, name='services'),
    # path('news/', mainapp.news, name='news'),
    # path('team/', mainapp.team, name='team'),