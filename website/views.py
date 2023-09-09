from django.contrib import messages
from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import Prefetch
from django.views.generic import FormView, ListView
from django.urls import reverse

from shop.models import Product, Image
from shop.selectors import highest_price_products_selector
from utils.send_email import send_html_email
from . forms import ContactForm
from . models import Contact


class ContactUsView(FormView):
    template_name = 'contact.html'
    model = Contact
    success_url = '/contact-us/'
    form_class = ContactForm

    def form_valid(self, form):
        contact, _ = Contact.objects.get_or_create(
            email=form.cleaned_data['email'],
            defaults={
                'name': form.cleaned_data['name'],
                'message': form.cleaned_data['message']
            }
        )
        message = f'Thank you for your message! {contact.name.title()}'

        send_html_email(
            subject='Thank you for your message!',
            to_email=[contact.email],
            message=message,
            template_name='emails/contact.html',
            context={
                'index_link': self.request.build_absolute_uri(reverse('index')),
                'women_link': self.request.build_absolute_uri(
                    reverse('catalog', kwargs={'slug': 'vona'})
                ),
                'men_link': self.request.build_absolute_uri(
                    reverse('catalog', kwargs={'slug': 'vin'})
                ),
                'message': message,
                'products': highest_price_products_selector()
            }
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Thank you {form.cleaned_data.get('name').upper()} "
            "for your message!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.WARNING,
            "Please send correct data"
        )
        return super().form_invalid(form)


class SearchView(ListView):
    template_name = 'shop-sidebar.html'
    model = Product
    context_object_name = 'prods'
    paginate_by = 9
    search_query = None

    def get(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search2')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=Image.objects.order_by('-size')
            )
        ).annotate(
            similarity=self._create_word_similarity()
        ).filter(
            similarity__gte=0.3
        ).order_by(
            '-similarity'
        )

    def _create_word_similarity(self):
        return TrigramWordSimilarity(self.search_query, 'title')
