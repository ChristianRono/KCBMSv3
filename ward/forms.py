from django import forms
from django.forms import ModelForm

from applicant.models import Application

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Enter Your Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Enter Your Password'}))

class WardAdminForm(ModelForm):
    
    class Meta:
        model =  Application
        fields = ('id','is_awarded','reasons','amount')

