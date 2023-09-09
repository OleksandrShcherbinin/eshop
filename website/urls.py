from django.urls import path

from .views import ContactUsView, SearchView


urlpatterns = [
    path('contact-us/', ContactUsView.as_view(), name='contact'),
    path('search/', SearchView.as_view(), name='search'),
]
