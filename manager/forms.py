from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import News


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Логин',)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['publicationTitle', 'publicationText']