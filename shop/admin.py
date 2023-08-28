from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from shop.models import Category, Product, Brand, Color, Size, Image


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products', 'picture')
    search_fields = ('name',)

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?brand__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')

    @staticmethod
    def picture(obj):
        return format_html(f'<img src="{obj.logo.url}" style="max-width: 50px">')


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?colors__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?categories__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('picture',)

    @staticmethod
    def picture(obj):
        return format_html(f'<img src="{obj.image.url}" style="max-width: 100px">')


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('image', 'picture')
    readonly_fields = ('picture',)
    extra = 0

    @staticmethod
    def picture(obj):
        return format_html(f'<img src="{obj.image.url}" style="max-width: 80px">')


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    inlines = (ImageInlineAdmin,)
    summernote_fields = ('description',)
    readonly_fields = ('discount',)
    list_display = ('title', 'price', 'old_price', 'discount')
    search_fields = ('name', 'description')
    list_filter = ('brand',)
    list_editable = ('price',)

    fieldsets = (
        (None, {
            'fields': (
                'source_url',
                ('title', 'slug'),
                ('description',),
                ('price', 'old_price', 'discount'),
                ('brand',),
                ('categories', 'colors', 'sizes'),
            )
        }),
    )


admin.site.site_header = 'Django Shop'
admin.site.site_title = 'Django Shop'
admin.site.index_title = 'Django Shop'
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size)
admin.site.register(Image, ImageAdmin)
