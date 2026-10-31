from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Avg, Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView
from store.forms import CheckoutForm, LaptopProductFilterForm, ProductReviewForm, RegistrationForm
from store.models import Category, Order, OrderItem, Product, Review


def _session_cart(request):
    cart = request.session.get('cart', {})
    return cart if isinstance(cart, dict) else {}


def _cart_count(request):
    return sum(
        quantity
        for quantity in _session_cart(request).values()
        if isinstance(quantity, int) and not isinstance(quantity, bool) and quantity > 0
    )


def _get_cart_items(request):
    cart = _session_cart(request)
    products = Product.objects.filter(
        pk__in=[int(product_id) for product_id in cart if str(product_id).isdigit()],
        is_active=True,
    )
    items = []
    for product in products:
        quantity = cart.get(str(product.pk), 0)
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            continue
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity,
            'available': quantity <= product.stock_quantity,
        })
    return items


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Головна показує опубліковані товари та всі категорії з бази даних.
        context['products'] = Product.objects.filter(is_active=True).select_related('category')
        context['categories'] = Category.objects.all()
        context['cart_count'] = _cart_count(self.request)
        return context


class CategoryProductsView(TemplateView):
    # Сторінка каталогу відбирає товари за категорією з адреси сторінки.
    template_name = 'home_laptops.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        context['categories'] = Category.objects.all()
        context['cart_count'] = _cart_count(self.request)
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


class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'

    specification_fields = (
        'manufacturer',
        'laptop_type',
        'display_diagonal',
        'resolution',
        'matrix_type',
        'screen_surface',
        'refresh_rate',
        'intel_generation',
        'amd_generation',
        'processor',
        'processor_cores',
        'ram_type',
        'ram_capacity',
        'ram_slots',
        'ssd_capacity',
        'graphics_type',
        'discrete_graphics_series',
        'video_memory',
        'wireless_technologies',
        'interfaces',
        'operating_system',
        'battery_capacity',
        'features',
        'weight',
        'color',
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(
            Product.objects.select_related('category'),
            pk=self.kwargs['product_id'],
            is_active=True,
        )
        context['product'] = product
        context['categories'] = Category.objects.all()
        context['cart_count'] = _cart_count(self.request)
        context['specifications'] = [
            (product._meta.get_field(field_name).verbose_name, getattr(product, field_name))
            for field_name in self.specification_fields
            if getattr(product, field_name)
        ]
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True,
        ).exclude(pk=product.pk)[:4]
        approved_reviews = product.reviews.filter(is_approved=True)
        rating = approved_reviews.aggregate(average=Avg('rating'))
        context['average_rating'] = rating['average'] or 0
        context['rating_stars'] = int(context['average_rating'] + 0.5)
        context['review_count'] = approved_reviews.count()
        context['reviews'] = approved_reviews
        context['review_form'] = ProductReviewForm(
            self.request.POST if self.request.method == 'POST' else None,
        )
        favorites = self.request.session.get('favorites', [])
        if not isinstance(favorites, list):
            favorites = []
        context['is_favorite'] = str(product.pk) in [str(value) for value in favorites]
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['review_form']
        if form.is_valid():
            Review.objects.create(
                product=context['product'],
                author_name=form.cleaned_data['author_name'],
                rating=int(form.cleaned_data['rating']),
                text=form.cleaned_data['text'],
            )
            messages.success(request, 'Дякуємо! Відгук з’явиться після перевірки.')
            return redirect('product_detail', product_id=context['product'].pk)
        return self.render_to_response(context, status=400)


def cart_view(request):
    items = _get_cart_items(request)
    total = sum((item['subtotal'] for item in items), Decimal('0.00'))
    return render(request, 'cart.html', {
        'items': items,
        'total': total,
        'cart_count': _cart_count(request),
        'can_checkout': bool(items) and all(item['available'] for item in items),
        'categories': Category.objects.all(),
    })


@require_POST
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = _session_cart(request).copy()
    current_quantity = cart.get(str(product.pk), 0)
    if not isinstance(current_quantity, int) or isinstance(current_quantity, bool):
        current_quantity = 0
    current_quantity = max(current_quantity, 0)

    if product.stock_quantity < 1:
        messages.error(request, 'Цього товару зараз немає в наявності.')
    elif current_quantity + 1 > product.stock_quantity:
        messages.error(request, 'У кошику вже максимальна доступна кількість цього товару.')
    else:
        cart[str(product.pk)] = current_quantity + 1
        request.session['cart'] = cart
        messages.success(request, 'Товар додано до кошика.')

    if request.POST.get('buy_now') == '1' and product.stock_quantity > 0:
        return redirect('checkout')
    next_url = request.POST.get('next_url', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return HttpResponseRedirect(next_url)
    return redirect('product_detail', product_id=product.pk)


@require_POST
def update_cart_view(request, product_id):
    cart = _session_cart(request).copy()
    product = get_object_or_404(Product, pk=product_id)
    quantity_value = request.POST.get('quantity', '')
    if not quantity_value.isdigit() or len(quantity_value) > 10:
        messages.error(request, 'Вкажи коректну кількість товару.')
    else:
        quantity = int(quantity_value)
        if quantity == 0:
            cart.pop(str(product.pk), None)
            messages.success(request, 'Товар видалено з кошика.')
        elif not product.is_active or quantity > product.stock_quantity:
            messages.error(request, f'Доступно лише {product.stock_quantity} шт. цього товару.')
        else:
            cart[str(product.pk)] = quantity
            messages.success(request, 'Кількість товару оновлено.')
        request.session['cart'] = cart
    return redirect('cart')


def checkout_view(request):
    items = _get_cart_items(request)
    total = sum((item['subtotal'] for item in items), Decimal('0.00'))
    if not items:
        messages.info(request, 'Кошик порожній.')
        return redirect('cart')
    if any(not item['available'] for item in items):
        messages.error(request, 'Перевір доступну кількість товарів у кошику.')
        return redirect('cart')

    form = CheckoutForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        product_ids = [item['product'].pk for item in items]
        with transaction.atomic():
            locked_products = {
                product.pk: product
                for product in Product.objects.select_for_update().filter(
                    pk__in=product_ids,
                    is_active=True,
                )
            }
            if any(
                item['product'].pk not in locked_products
                or item['quantity'] > locked_products[item['product'].pk].stock_quantity
                for item in items
            ):
                messages.error(request, 'Наявність товарів змінилася. Перевір кошик і спробуй ще раз.')
                return redirect('cart')

            order_total = sum(
                (locked_products[item['product'].pk].price * item['quantity'] for item in items),
                Decimal('0.00'),
            )
            order = Order.objects.create(
                **form.cleaned_data,
                total=order_total,
            )
            for item in items:
                product = locked_products[item['product'].pk]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=item['quantity'],
                    unit_price=product.price,
                )
                product.stock_quantity -= item['quantity']
                product.save(update_fields=['stock_quantity'])

        request.session['cart'] = {}
        request.session['last_order_id'] = order.pk
        return redirect('order_success')

    return render(request, 'checkout.html', {
        'form': form,
        'items': items,
        'total': total,
        'categories': Category.objects.all(),
        'cart_count': _cart_count(request),
    })


def order_success_view(request):
    order_id = request.session.get('last_order_id')
    if not order_id:
        return redirect('home')
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_success.html', {'order': order})


@require_POST
def toggle_favorite_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    favorites = request.session.get('favorites', [])
    if not isinstance(favorites, list):
        favorites = []
    favorites = [str(value) for value in favorites if str(value).isdigit()]
    if str(product.pk) in favorites:
        favorites.remove(str(product.pk))
        messages.success(request, 'Товар видалено з обраного.')
    else:
        favorites.append(str(product.pk))
        messages.success(request, 'Товар додано до обраного.')
    request.session['favorites'] = favorites
    if request.POST.get('next_url') == 'favorites':
        return redirect('favorites')
    return redirect('product_detail', product_id=product.pk)


def favorites_view(request):
    favorites = request.session.get('favorites', [])
    if not isinstance(favorites, list):
        favorites = []
    products = Product.objects.filter(
        pk__in=[int(value) for value in favorites if str(value).isdigit()],
        is_active=True,
    ).select_related('category')
    return render(request, 'favorites.html', {
        'products': products,
        'categories': Category.objects.all(),
        'cart_count': _cart_count(request),
    })


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