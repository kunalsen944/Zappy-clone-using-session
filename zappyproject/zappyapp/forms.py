from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class CustomerUpdate(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['images','cust_address','mobile',]
