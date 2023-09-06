from django.urls import path

from .views import ContactUsView

urlpatterns = [
    path('contact-us/', ContactUsView.as_view(), name='contact'),
]
