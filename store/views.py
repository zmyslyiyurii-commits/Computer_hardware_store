from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic import CreateView, TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

class LoginView(DjangoLoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Введи ім’я користувача',
            'autocomplete': 'username',
        })
        form.fields['password'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Введи свій пароль',
            'autocomplete': 'current-password',
        })
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Вітаємо, {self.request.user.username}! Ви увійшли.')
        return response

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Придумай ім’я користувача',
            'autocomplete': 'username',
        })
        form.fields['password1'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Придумай надійний пароль',
            'autocomplete': 'new-password',
        })
        form.fields['password2'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Введи пароль ще раз',
            'autocomplete': 'new-password',
        })
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Акаунт створено. Вітаємо, {self.object.username}!')
        return response