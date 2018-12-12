from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
