from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from django import forms

from .models import User


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class ContactForm(ModelForm):
    class Meta:
        model = User
        fields = ["user_name", "user_email"]
        widgets = {
            'user_name': TextInput(attrs={'class': 'form-control'}),
            'user_email': EmailInput(attrs={'class': 'form-control'})
        }

class ConnexionForm(forms.Form):
    username = forms.CharField(label="User name", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)