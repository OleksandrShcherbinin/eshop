from django.db.models import QuerySet
from django.urls import reverse

from shop.selectors import lowest_price_products_selector
from utils.send_email import send_html_email
from website.models import Contact


def contact_mailing(modeladmin, request, queryset: QuerySet[Contact]):
    for obj in queryset:
        message = f'Hello {obj.name}'
        send_html_email(
            subject='Welcome to our website! We have greate proposal to you!',
            to_email=[obj.email],
            message=message,
            template_name='emails/distribution.html',
            context={
                'index_link': request.build_absolute_uri(reverse('index')),
                'women_link': request.build_absolute_uri(
                    reverse('catalog', kwargs={'slug': 'vona'})
                ),
                'men_link': request.build_absolute_uri(
                    reverse('catalog', kwargs={'slug': 'vin'})
                ),
                'message': message,
                'products': lowest_price_products_selector()[:4]
            }
        )


contact_mailing.short_description = 'Електронна розсилка для контактів'
