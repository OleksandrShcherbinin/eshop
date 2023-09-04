from typing import Any

from django.db.models import Prefetch, Max, Min
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from . models import Category, Image, Product
from .selectors import (
    lowest_price_products_selector,
    highest_price_products_selector, product_main_images_selector,
    single_product_featured_items_selector,
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'lowest_price_products': lowest_price_products_selector(),
            'highest_price_products': highest_price_products_selector()
        }

        return context


class FullCatalog(ListView):
    template_name = 'shop-sidebar.html'
    model = Product
    context_object_name = 'prods'
    slug_url_kwarg = 'slug'
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=Image.objects.order_by('-size')
            )
        )


class Catalog(ListView):
    template_name = 'shop-sidebar.html'
    model = Product
    context_object_name = 'prods'
    slug_url_kwarg = 'slug'
    paginate_by = 9

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Product.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=Image.objects.order_by('-size')
            )
        ).filter(categories=category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'prices': Product.objects.aggregate(
                max=Max('price'),
                min=Min('price')
            ),
        }
        return context


class ProductView(DetailView):
    template_name = 'single-product.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    queryset = Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    ).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'main_images': product_main_images_selector(self.object),
            'featured_items': single_product_featured_items_selector(self.object)
        }
        return context
