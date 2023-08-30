from django.shortcuts import render, get_object_or_404

from . models import Category, Product


def index(request):
    context = {}
    return render(request, 'index.html', context=context)


def catalog(request, **kwargs):
    category = get_object_or_404(Category, slug=kwargs.get('slug'))
    products = Product.objects.filter(categories=category)[:9]
    context = {
        'prods': products
    }
    return render(request, 'shop-sidebar.html', context)


def product(request):
    context = {}
    return render(request, 'single-product.html', context)
