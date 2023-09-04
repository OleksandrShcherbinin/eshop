from django.db.models import QuerySet, Prefetch

from shop.models import Product, Image


def lowest_price_products_selector() -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    ).order_by('price')[:8]


def highest_price_products_selector() -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    ).order_by('-price')[:4]


def product_main_images_selector(product: Product) -> QuerySet[Image]:
    return Image.objects.filter(product=product).order_by('-size')[:4]


def single_product_featured_items_selector(product: Product) -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    ).filter(
        categories__in=product.categories.all()
    ).exclude(
        pk=product.pk
    ).order_by('-price')[:4]
