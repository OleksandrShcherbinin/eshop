from django.db import models

from .abstact_models import Subscribable


class Subscribe(Subscribable):

    def __str__(self):
        return self.email


class Contact(Subscribable):
    name = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
