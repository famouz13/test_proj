from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'address', 'phone_number')
    list_filter = ('first_name', 'phone_number', 'address')

    def fullname(self, obj):
        return f'{obj.first_name} {obj.second_name}'
