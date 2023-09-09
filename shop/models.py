from decimal import Decimal
from django.db import models

from .abstract_model import TimestampedModel


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category name')
    slug = models.SlugField(max_length=70, unique=True, verbose_name='Slug')
    image = models.ImageField(
        upload_to='images/category',
        blank=True, null=True,
        verbose_name='Image'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, verbose_name='Size name')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(
        max_length=50, unique=True,
        verbose_name='Color name'
    )
    hex_code = models.CharField(
        max_length=7,
        blank=True,
        default='',
        verbose_name='Hex code'
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Brand name'
    )
    logo = models.ImageField(
        upload_to='images/brand',
        blank=True, null=True,
        verbose_name='Image'
    )

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='images/product', max_length=300)
    url = models.URLField(max_length=512, verbose_name='Image URL')
    size = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.image.url


class Product(TimestampedModel):
    source_url = models.URLField(max_length=512, verbose_name='Source URL')
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    description = models.TextField(
        blank=True, default='',
        verbose_name='Description'
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, null=True,
        verbose_name='Price'
    )
    old_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, null=True,
        verbose_name='Price before sale'
    )
    discount = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, null=True,
        verbose_name='Discount'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True, blank=True,
    )
    categories = models.ManyToManyField(
        Category,
        related_name='products',
    )
    colors = models.ManyToManyField(
        Color,
        related_name='products',
    )
    sizes = models.ManyToManyField(
        Size,
        related_name='products',
    )

    def save(self, *args, **kwargs) -> None:
        if self.old_price:
            self.discount = Decimal(
                round((float(self.price) / float(self.old_price))
                      * 100 - 100, 2)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
