from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        # widgets = {'id': forms.HiddenInput()}
        fields = ['id', 'first_name', 'second_name', 'address', 'phone_number']

        labels = {
            'first_name': 'Имя',
            'second_name': 'Фамиля',
            'address': 'Адрес',
            'phone_number': 'Номер телефона',
        }
