"""
Используемые модули
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import News
from .models import RegManager
from martor.fields import MartorFormField


class EditProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля
    """
    username = forms.CharField(required=True, label='Логин',)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CreateNewsForm(forms.ModelForm):
    """
    Форма создания новостей
    """
    publicationText = MartorFormField()
    
    class Meta:
        model = News
        # manager/forms.py
        fields = ['publicationTitle', 'publicationText', 'donation_on']


class RegManagerForm(forms.ModelForm):
    """
    Форма регистрации менеджера
    """
    class Meta:
        model = RegManager
        fields = ('fullName', 'userEmail', 'ukEmail', 'appointment', 'phoneNumber')
        # manager/forms.py
