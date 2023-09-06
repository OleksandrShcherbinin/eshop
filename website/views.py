from django.contrib import messages
from django.views.generic import FormView

from utils.send_email import send_email
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
        send_email(
            subject='Thank you for your message!',
            to_email=[contact.email],
            message=f'Thank you for your message! {contact.name.title()}'
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
