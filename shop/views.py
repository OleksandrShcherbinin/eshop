from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from . models import Category, Product
from .selectors import (
    lowest_price_products_selector,
    highest_price_products_selector,
    product_main_images_selector,
    single_product_featured_items_selector,
    product_prefetched_images_by_size_selector,
    min_max_product_prices_selector,
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'lowest_price_products': lowest_price_products_selector()[:8],
            'highest_price_products': highest_price_products_selector()[:4],
            'all_categories': Category.objects.all(),
        }

        return context


class FullCatalog(ListView):
    template_name = 'shop-sidebar.html'
    model = Product
    context_object_name = 'prods'
    slug_url_kwarg = 'slug'
    paginate_by = 9

    def get_queryset(self):
        return product_prefetched_images_by_size_selector().all()


class Catalog(ListView):
    template_name = 'shop-sidebar.html'
    model = Product
    context_object_name = 'prods'
    slug_url_kwarg = 'slug'
    paginate_by = 9

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return product_prefetched_images_by_size_selector().filter(
            categories=category
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'prices': min_max_product_prices_selector(),
        }
        return context


class ProductView(DetailView):
    template_name = 'single-product.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    queryset = product_prefetched_images_by_size_selector().all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'main_images': product_main_images_selector(self.object)[:4],
            'featured_items': single_product_featured_items_selector(
                self.object
            )[:4]
        }
        return context
