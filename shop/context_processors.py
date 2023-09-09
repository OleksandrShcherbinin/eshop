from .selectors import (
    most_products_categories_selector,
    best_price_categories_selector,
)


def header_categories(request):
    return {
        'categories': most_products_categories_selector()[:15],
        'best_price_categories': best_price_categories_selector()[:15]
    }
