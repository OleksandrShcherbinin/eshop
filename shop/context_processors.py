from django.db.models import Count, Avg

from . models import Category


def header_categories(request):
    top_categories = Category.objects.annotate(
        products_count=Count('products')
    ).order_by('-products_count')[:15]
    best_price_categories = Category.objects.annotate(
        average_prices=Avg('products__price')
    ).order_by('average_prices')[:15]
    return {
        'categories': top_categories,
        'best_price_categories': best_price_categories
    }
