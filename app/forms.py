"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Käyttäjätunnus'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Salasana'}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput','placeholder':'Käyttäjätunnus'}),
            'email': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput','placeholder':'Sähköposti'}),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'