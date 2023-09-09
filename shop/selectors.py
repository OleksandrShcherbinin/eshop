from decimal import Decimal

from django.db.models import Avg, Count, QuerySet, Prefetch

from shop.models import Category, Product, Image


def most_products_categories_selector() -> QuerySet[Category]:
    return Category.objects.annotate(
        products_count=Count('products')
    ).order_by(
        '-products_count'
    )


def best_price_categories_selector() -> QuerySet[Category]:
    return Category.objects.annotate(
        average_prices=Avg('products__price')
    ).order_by(
        'average_prices'
    )


def lowest_price_products_selector() -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    ).order_by('price')


def highest_price_products_selector() -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    ).order_by('-price')


def product_main_images_selector(product: Product) -> QuerySet[Image]:
    return Image.objects.filter(product=product).order_by('-size')


def product_prefetched_images_by_size_selector() -> QuerySet[Product]:
    return Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=Image.objects.order_by('-size')
        )
    )


def single_product_featured_items_selector(
        product: Product
) -> QuerySet[Product]:
    return product_prefetched_images_by_size_selector().filter(
        categories__in=product.categories.all()
    ).exclude(
        pk=product.pk
    ).order_by('-price')


def min_max_product_prices_selector() -> dict[str, Decimal]:
    return Product.objects.aggregate(
        max=Avg('price'),
        min=Avg('price')
    )
