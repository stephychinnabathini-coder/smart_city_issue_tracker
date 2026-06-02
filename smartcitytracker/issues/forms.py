from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Issue

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description", "category", "severity", "photo", "video", "latitude", "longitude", "address"]

        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
