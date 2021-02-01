from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from directory.forms import ContactForm
from directory.models import Contact
from django.db.models import Q
from django.views.generic import RedirectView, TemplateView, CreateView


class ContactsView(TemplateView):
    template_name = 'directory/abonents.html'
    pattern_name = 'contacts'

    def get_context_data(self, contacts, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = contacts
        return context

    def get(self, request):
        contacts = []
        if (key := request.GET.get('key')):
            contacts = Contact.objects.all().filter(
                Q(first_name__contains=key) | Q(phone_number__contains=key))
            if not contacts:
                messages.info(request, 'Не найдено контактов по данному поиску!')
        else:
            contacts = Contact.objects.all()
        return self.render_to_response(self.get_context_data(contacts))


class ContactView(TemplateView):
    template_name = 'directory/abonent.html'
    pattern_name = 'contacts/<int:id>'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.get(pk=id)
        return context

    def get(self, request, id):
        cont = Contact.objects.get(pk=id)
        form = ContactForm(initial=cont.__dict__)
        return self.render_to_response(self.get_context_data(id, form=form))

    def post(self, request, id):
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                contact_to_edit = Contact.objects.get(pk=request.POST.get('id'))
                contact_to_edit.first_name = form.cleaned_data['first_name']
                contact_to_edit.second_name = form.cleaned_data['second_name']
                contact_to_edit.address = form.cleaned_data['address']
                contact_to_edit.phone_number = form.cleaned_data['phone_number']
                contact_to_edit.save()
                messages.info(request, 'contact edited!')
                self.render_to_response(self.get_context_data(id))
        except Exception as e:
            print(e)
            messages.info(request, 'error while editing contact')
        return self.render_to_response(self.get_context_data(id, form=form))


class CreateContactView(TemplateView):
    template_name = 'directory/add.html'
    pattern_name = 'contact_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request):
        form = ContactForm()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request):
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                Contact.objects.create(**create_contact_dict(create_contact_dict(form.cleaned_data)))
                messages.info(request, 'contact created!')
        except Exception as e:
            messages.info(request, 'error while creating contact!')
        return self.render_to_response(self.get_context_data(form=form))


class ContactDeleteView(TemplateView):
    template_name = 'directory/abonents.html'
    pattern_name = 'contact_delete'

    def get(self, request, id):
        try:
            Contact.objects.filter(pk=id).delete()
            messages.info(request, 'Contact deleted!')
        except:
            messages.info(request, 'Error while deleting contact!')
        return self.render_to_response({})


def create_contact_dict(data):
    return {
        'first_name': data.get('first_name'),
        'second_name': data.get('second_name'),
        'address': data.get('address'),
        'phone_number': data.get('phone_number'),
    }


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('contacts')
    template_name = 'registration/register.html'

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        return self.get(request)
