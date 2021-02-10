"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm
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
    password = forms.CharField(label=_("Salasana"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Salasana'}))

class CreateGroup(forms.Form):
    groupname = forms.CharField(label='Ryhmän nimi', max_length=50,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Porukan nimi'}))

class JoinGroup(forms.Form):
    groupname = forms.CharField(label='Kutsukoodi', max_length=50,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Kutsukoodi'}))


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

class AddeventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["name", "type", "description","max","date","group"] #'__all__'#["username", "email", "password1", "password2"]

        #widgets = {
        #    'username': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput','placeholder':'Käyttäjätunnus'}),
        #    'email': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput','placeholder':'Sähköposti'}),
        #    'password1': forms.PasswordInput(),
        #    'password2': forms.PasswordInput(),
        #}
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        #print(user)
        super(AddeventForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['group'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['max'].widget.attrs['class'] = 'form-control'
        #self.fields['date'].widget.attrs['id'] = 'datetime-local'
        self.fields['date'].widget = forms.DateTimeInput({
                                   'class': 'form-control',
                                   'name': 'date',
                                   'type' : 'datetime-local',
                                   'id':'datetime-local'})
        if user:
            #print(user.username)
            try:
                userq = Person.objects.get(username=user.username)
                #print(Group.objects.all())
                #print(user.groups.all())
                #groups = Group.objects.all().filter(user__id__in=userq.all())
                self.fields['group'].queryset = userq.groups.all()
                print(self.fields['group'].queryset)
            except:
                pass
        #self.fields['date'].widget.attrs['type'] = 'datetime-local'

