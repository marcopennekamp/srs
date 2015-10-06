from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)