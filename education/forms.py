# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from education.models import KCBMSUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = KCBMSUser
        fields = ("username", "email",'is_ward_admin','is_edu_admin','is_accountant')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = KCBMSUser
        fields = ("username", "email",'is_ward_admin','is_edu_admin','is_accountant')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Enter Your Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Enter Your Password'}))
