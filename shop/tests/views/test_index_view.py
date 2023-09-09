from django.test import TestCase
from django.urls import reverse
from model_bakery import baker


class IndexViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.products = baker.make('shop.Product', _quantity=10)

    def test_get(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(
            len(response.context['lowest_price_products']), 8
        )
        self.assertEqual(
            len(response.context['highest_price_products']), 4
        )
        self.assertContains(response, 'Explore our Products')
        self.assertContains(response, 'Browse by Category')
        self.assertContains(response, 'New Arrivals')
