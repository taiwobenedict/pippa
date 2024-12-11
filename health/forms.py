from django import forms
from .models import *


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', "last_name", "email", "sex", 'age', 'location', "password", "confirm_password"]


class LoginForm(forms.Form):
    email = forms.CharField(max_length=50, widget=forms.EmailInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    
        
