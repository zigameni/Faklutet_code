from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Form
from django import forms

from vesti.models import Korisnik, Vest


class KorisnikCreationForm(UserCreationForm):

    class Meta:
        model = Korisnik;
        fields = ['username', 'password1', 'password2']


class VestForm(ModelForm):
    class Meta:
        model = Vest
        exclude = ['autor']

class SearchForm(Form):
    term = forms.CharField(max_length=50);
