from django.urls import path

from .views import index, catalog, product

urlpatterns = [
    path('', index, name='index'),
    path('catalog/<slug:slug>/', catalog, name='catalog'),
    path('product/', product, name='product'),
]
