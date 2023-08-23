from django.urls import path

from .views import index, catalog

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
]
