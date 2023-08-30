from django.db.models import Count

from . models import Category


def header_categories(request):
    categories = Category.objects.annotate(
        products_count=Count('products')
    ).order_by('-products_count')[:10]
    return {
        'categories': categories
    }
