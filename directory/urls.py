from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactsView.as_view(), name='contacts'),
    path('<int:id>', views.ContactView.as_view(), name='contact'),
    path('add', views.CreateContactView.as_view(), name='contact_add'),
    path('delete/<int:id>', views.ContactDeleteView.as_view(), name='contact_delete'),
]
