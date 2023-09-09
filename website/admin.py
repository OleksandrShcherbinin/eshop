from django.contrib import admin

from .actions import contact_mailing
from .models import Contact, Subscribe


class ContactAdmin(admin.ModelAdmin):
    actions = (contact_mailing,)
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Subscribe)
