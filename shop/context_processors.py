from django.db.models import Count

from . models import Category


def header_categories(request):
    top_categories = Category.objects.annotate(
        products_count=Count('products')
    ).order_by('-products_count')[:15]
    return {
        'categories': top_categories
    }
