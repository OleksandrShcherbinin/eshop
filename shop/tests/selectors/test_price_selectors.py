from decimal import Decimal

from django.test import TestCase
from model_bakery import baker

from shop.selectors import (
    lowest_price_products_selector,
    highest_price_products_selector, most_products_categories_selector,
    best_price_categories_selector,
)


class PriceSelectorsTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        for i in range(1, 11):
            baker.make('shop.Product', price=i * 100)

    def test_lowest_price_products_selector(self):
        products = lowest_price_products_selector()

        self.assertEqual(products.count(), 10)
        self.assertEqual(products.first().price, Decimal(100))
        self.assertEqual(products[9].price, Decimal(1000))

    def test_highest_price_products_selector(self):
        products = highest_price_products_selector()

        self.assertEqual(products.count(), 10)
        self.assertEqual(products.first().price, Decimal(1000))
        self.assertEqual(products[9].price, Decimal(100))


class CategoriesSelectorsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.categories = []
        for i in range(1, 11):
            category = baker.make('shop.Category', name=f'Category {i}')
            cls.categories.append(category)
            for j in range(1, i + 1):
                baker.make(
                    'shop.Product',
                    price=i * j * 100,
                    categories=[category]
                )

    def test_most_products_categories_selector(self):
        categories = most_products_categories_selector()

        self.assertEqual(categories.count(), 10)
        self.assertEqual(categories.first().products_count, 10)
        self.assertEqual(categories[9].products_count, 1)

    def test_best_price_categories_selector(self):
        categories = best_price_categories_selector()

        self.assertEqual(categories.count(), 10)
        self.assertEqual(categories.first().average_prices, Decimal(100))
        self.assertEqual(categories[9].average_prices, Decimal(5500))
