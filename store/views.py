from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, TemplateView
from store.forms import LaptopProductFilterForm, RegistrationForm
from store.models import Category, Product


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Головна показує опубліковані товари та всі категорії з бази даних.
        context['products'] = Product.objects.filter(is_active=True).select_related('category')
        context['categories'] = Category.objects.all()
        return context


class CategoryProductsView(TemplateView):
    # Сторінка каталогу відбирає товари за категорією з адреси сторінки.
    template_name = 'home_laptops.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        context['categories'] = Category.objects.all()
        context['category'] = category
        # Для назви сторінки використовуємо узгоджену множину, навіть якщо
        # категорію в адмінці поки названо в однині.
        context['category_title'] = (
            'Ноутбуки'
            if category.name.strip().casefold().startswith('ноутбук')
            else category.name
        )
        context['products'] = Product.objects.filter(
            category=category,
            is_active=True,
        ).select_related('category')
        context['filter_groups'] = ()
        context['laptop_filter_form'] = None
        context['placeholder_filter_groups'] = ()
        if category.name.strip().casefold().startswith('ноутбук'):
            base_products = context['products']
            filter_form = LaptopProductFilterForm(
                self.request.GET or None,
                products=base_products,
            )
            if filter_form.is_valid():
                cleaned_data = filter_form.cleaned_data
                if cleaned_data['price_min'] is not None:
                    context['products'] = context['products'].filter(
                        price__gte=cleaned_data['price_min'],
                    )
                if cleaned_data['price_max'] is not None:
                    context['products'] = context['products'].filter(
                        price__lte=cleaned_data['price_max'],
                    )
                for field_name, _ in filter_form.filter_fields:
                    selected_values = cleaned_data[field_name]
                    if selected_values:
                        if field_name in filter_form.multi_value_fields:
                            matching_values = Q()
                            for value in selected_values:
                                matching_values |= (
                                    Q(**{f'{field_name}__iexact': value})
                                    | Q(**{f'{field_name}__istartswith': f'{value},'})
                                    | Q(**{f'{field_name}__icontains': f', {value},'})
                                    | Q(**{f'{field_name}__icontains': f',{value},'})
                                    | Q(**{f'{field_name}__iendswith': f', {value}'})
                                    | Q(**{f'{field_name}__iendswith': f',{value}'})
                                )
                            context['products'] = context['products'].filter(matching_values)
                        else:
                            context['products'] = context['products'].filter(
                                **{f'{field_name}__in': selected_values},
                            )

            context['laptop_filter_form'] = filter_form
            context['filter_groups'] = filter_form.filter_groups
            # Решта характеристик поки показується як заглушка до наступного етапу.
            context['placeholder_filter_groups'] = (
                'Серія (модельний ряд)',
            )
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


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
        # Після успішного входу показуємо користувачу повідомлення.
        response = super().form_valid(form)
        messages.success(self.request, f'Вітаємо, {self.request.user.username}! Ви увійшли.')
        return response


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Придумай ім’я користувача',
            'autocomplete': 'username',
        })
        form.fields['last_name'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Введи своє прізвище',
            'autocomplete': 'family-name',
        })
        form.fields['email'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'name@example.com',
            'autocomplete': 'email',
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
        # Після реєстрації одразу авторизуємо новий обліковий запис.
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Акаунт створено. Вітаємо, {self.object.username}!')
        return response