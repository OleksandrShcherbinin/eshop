from django.urls import path

from .views import IndexView, FullCatalog, catalog, product

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', FullCatalog.as_view(), name='full_catalog'),
    path('catalog/<slug:slug>/', catalog, name='catalog'),
    path('product/<slug:slug>/', product, name='product'),
]
