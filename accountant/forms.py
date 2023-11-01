from django import forms

class EmailForm(forms.Form):
    to = forms.EmailField()
    re = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Enter Your Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Enter Your Password'}))
