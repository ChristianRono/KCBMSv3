# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from education.models import KCBMSUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = KCBMSUser
        fields = ("username", "email",'is_ward_admin','is_edu_admin','is_accountant')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = KCBMSUser
        fields = ("username", "email",'is_ward_admin','is_edu_admin','is_accountant')