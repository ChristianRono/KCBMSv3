from django import forms
from django.forms import ModelForm

from applicant.models import Application,Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Enter Your Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Enter Your Password'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Enter Your Username'}))
    email = forms.EmailField(max_length=20, widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Enter Your Email'}))
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'id': 'password1', 'placeholder': 'Enter Your Password'}))
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'id': 'password2', 'placeholder': 'Confirm Your Password'}))

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = [
            "fee_balance",
            "fee_statement",
            "previous_term_report",
        ]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "admission_number",
            "parents_name",
            "parents_phone",
            "parents_id",
            "school_name",
            "bank_name",
            "bank_account",
            "bank_branch",
            "course",
            "year_of_study",
            "year_of_completion",
            "disability_status",
            "family_status",
            "death_certificate_father",
            "death_certificate_mother",
            "applied_bursary_before",
            "annual_school_fees",
            "ward",
            "family_income"
        ]