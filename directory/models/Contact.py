from django.db import models as m
from django.core.validators import MinLengthValidator, RegexValidator


class Contact(m.Model):
    first_name = m.CharField(verbose_name='First name', max_length=30, validators=[MinLengthValidator(2)])
    second_name = m.CharField(verbose_name='Second name', max_length=30, validators=[MinLengthValidator(2)])
    address = m.CharField(verbose_name='Address', max_length=50, validators=[MinLengthValidator(2)])

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. ")
    phone_number = m.CharField(verbose_name='Phone', max_length=15, validators=[phone_regex])

    def __str__(self):
        return f'Firstname: {self.first_name} | SecondName: {self.second_name} | address: {self.address} | Phone: {self.phone_number}'

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        # constraints = (m.UniqueConstraint(fields=['phone_number'], name='phone_unique'),)
