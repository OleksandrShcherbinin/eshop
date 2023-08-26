from django.contrib import admin

from shop.models import Category, Product, Brand, Color, Size, Image


admin.site.site_header = 'Django Shop'
admin.site.site_title = 'Django Shop'
admin.site.index_title = 'Django Shop'
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Image)
admin.site.register(Product)
