from django.urls import path

from .views import IndexView, FullCatalog, Catalog, ProductView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', FullCatalog.as_view(), name='full_catalog'),
    path('catalog/<slug:slug>/', Catalog.as_view(), name='catalog'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product'),
]
