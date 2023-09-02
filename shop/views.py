from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from . models import Category, Image, Product


class IndexView(TemplateView):
    template_name = 'index.html'


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


def catalog(request, **kwargs):
    category = get_object_or_404(Category, slug=kwargs.get('slug'))
    products = Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    ).filter(categories=category)[:9]
    context = {
        'prods': products
    }
    return render(request, 'shop-sidebar.html', context)


def product(request, **kwargs):
    single_product = get_object_or_404(Product, slug=kwargs.get('slug'))
    main_images = Image.objects.filter(product=single_product).order_by('-size')[:4]
    featured_products = Product.objects.filter(
        categories__in=single_product.categories.all()
    ).order_by('-price')[:8]
    context = {
        'product': single_product,
        'main_images': main_images,
        'featured_items': featured_products
    }
    return render(request, 'single-product.html', context)
