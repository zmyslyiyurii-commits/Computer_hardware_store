from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    last_name = forms.CharField(
        label='Прізвище',
        max_length=150,
        required=True,
    )
    email = forms.EmailField(
        label='Електронна пошта',
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'last_name', 'email')
