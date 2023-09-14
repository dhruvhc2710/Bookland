from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import Seller


class SellerForm(forms.ModelForm):

    class Meta:
        model = Seller
        fields = ['BookSet_Photo', 'Subjects', 'Description', 'Key', 'Total_Price']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("This password must contain at least 8 characters.")
        return password