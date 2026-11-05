from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView
from store.forms import (
    CheckoutForm,
    ComputerProductFilterForm,
    LaptopProductFilterForm,
    MotherboardProductFilterForm,
    ProcessorProductFilterForm,
    ProductReviewForm,
    ProfileDetailsForm,
    RegistrationForm,
    VideoCardProductFilterForm,
)
from store.models import Category, CustomerProfile, Order, OrderItem, Product, Review


def _session_cart(request):
    cart = request.session.get('cart', {})
    return cart if isinstance(cart, dict) else {}


def _cart_count(request):
    return sum(
        quantity
        for quantity in _session_cart(request).values()
        if isinstance(quantity, int) and not isinstance(quantity, bool) and quantity > 0
    )


def _favorite_ids(request):
    favorites = request.session.get('favorites', [])
    if not isinstance(favorites, list):
        return []
    return [int(value) for value in favorites if str(value).isdigit()]


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


def _is_computer_components_category(category):
    return category.name.strip().casefold().replace("'", '’') == 'комплектуючі для пк'


def _search_products(query):
    products = Product.objects.filter(is_active=True).select_related('category')
    for term in query.split():
        products = products.filter(
            Q(name__icontains=term)
            | Q(manufacturer__icontains=term)
            | Q(model_series__icontains=term)
            | Q(description__icontains=term)
            | Q(category__name__icontains=term)
        )
    return products


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if query:
            category = Category.objects.filter(name__iexact=query).first()
            if category:
                if _is_computer_components_category(category):
                    return redirect('computer_components', category_id=category.pk)
                return redirect(
                    'category_products',
                    category_id=category.pk,
                )

            matching_products = _search_products(query)
            exact_products = matching_products.filter(name__iexact=query)
            exact_product = exact_products.first()
            if exact_product and not exact_products.exclude(pk=exact_product.pk).exists():
                return redirect('product_detail', product_id=exact_product.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        active_products = Product.objects.filter(
            is_active=True,
        ).select_related('category')
        products = _search_products(query) if query else active_products
        context['popular_products'] = (
            products if query else active_products.filter(is_featured=True)
        )
        context['other_products'] = (
            active_products.filter(is_featured=False) if not query else Product.objects.none()
        )
        context['products'] = products
        context['search_query'] = query
        context['categories'] = Category.objects.all()
        context['cart_count'] = _cart_count(self.request)
        context['favorite_ids'] = _favorite_ids(self.request)
        return context


class ComputerComponentsView(TemplateView):
    template_name = 'computer_components.html'

    component_cards = (
        (
            'processor',
            'Процесори',
            'Обчислювальна основа комп’ютера',
            'https://brain.com.ua/static/images/prod_img/4/6/U0648246_1739383570.webp',
        ),
        (
            'motherboard',
            'Материнські плати',
            'З’єднує всі компоненти системи',
            'https://brain.com.ua/static/images/prod_img/9/2/U0763992_1738792930.webp',
        ),
        (
            'graphics_card',
            'Відеокарти',
            'Для ігор, графіки та 3D',
            'https://brain.com.ua/static/images/prod_img/9/6/U1043496_1747713905.webp',
        ),
        (
            'memory',
            "Оперативна пам’ять",
            'Пам’ять для швидкої роботи системи',
            'https://brain.com.ua/static/images/prod_img/0/5/U0559405_1739809983.webp',
        ),
        (
            'storage',
            'Накопичувачі SSD / HDD',
            'Для системи, програм і файлів',
            'https://brain.com.ua/static/images/prod_img/0/6/U0953606_1738404203.webp',
        ),
        (
            'case',
            'Корпуси',
            'Основа для розміщення комплектуючих',
            'https://brain.com.ua/static/images/prod_img/8/2/U1124682_1779297576.webp',
        ),
        (
            'power_supply',
            'Блоки живлення',
            'Живлення всіх компонентів ПК',
            'https://brain.com.ua/static/images/prod_img/8/8/U0931088_1738344411.webp',
        ),
        (
            'cooling',
            'Системи охолодження',
            'Кулери та рідинне охолодження',
            'https://brain.com.ua/static/images/prod_img/2/4/U1081824_1753417226.jpg',
        ),
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category,
            pk=self.kwargs['category_id'],
            name='Комплектуючі для ПК',
        )
        counts = dict(
            Product.objects.filter(category=category, is_active=True)
            .values('component_type')
            .annotate(product_count=Count('pk'))
            .values_list('component_type', 'product_count')
        )
        context.update({
            'category': category,
            'categories': Category.objects.all(),
            'cart_count': _cart_count(self.request),
            'component_cards': [
                {
                    'type': component_type,
                    'title': title,
                    'description': description,
                    'image_url': image_url,
                    'product_count': counts.get(component_type, 0),
                }
                for component_type, title, description, image_url in self.component_cards
            ],
        })
        return context


class CategoryProductsView(TemplateView):
    # Сторінка каталогу відбирає товари за категорією з адреси сторінки.
    template_name = 'category_products.html'

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs['category_id'])
        if _is_computer_components_category(category):
            component_type = request.GET.get('component_type')
            valid_types = {value for value, _ in Product.COMPONENT_TYPE_CHOICES}
            if component_type not in valid_types:
                return redirect('computer_components', category_id=category.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        context['categories'] = Category.objects.all()
        context['cart_count'] = _cart_count(self.request)
        context['favorite_ids'] = _favorite_ids(self.request)
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
        if _is_computer_components_category(category):
            selected_type = self.request.GET['component_type']
            selected_title = dict(Product.COMPONENT_TYPE_CHOICES)[selected_type]
            context['products'] = context['products'].filter(component_type=selected_type)
            context['category_title'] = selected_title
            context['selected_component_type'] = selected_type
            context['selected_component_title'] = selected_title
            context['component_category'] = True
            context['processor_catalog'] = selected_type == 'processor'
            context['motherboard_catalog'] = selected_type == 'motherboard'
            context['video_card_catalog'] = selected_type == 'graphics_card'
        context['filter_groups'] = ()
        context['filter_form'] = None
        context['placeholder_filter_groups'] = ()
        normalized_category_name = category.name.strip().casefold().replace("'", '’')
        filter_form_class = None
        if normalized_category_name.startswith('ноутбук'):
            filter_form_class = LaptopProductFilterForm
        elif normalized_category_name == 'комп’ютери':
            filter_form_class = ComputerProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'processor'
        ):
            filter_form_class = ProcessorProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'motherboard'
        ):
            filter_form_class = MotherboardProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'graphics_card'
        ):
            filter_form_class = VideoCardProductFilterForm

        if filter_form_class:
            base_products = context['products']
            filter_form = filter_form_class(
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
                if (
                    isinstance(filter_form, MotherboardProductFilterForm)
                    and cleaned_data['available_today']
                ):
                    context['products'] = context['products'].filter(
                        motherboard_available_today=True,
                    )
                for field_name, _ in filter_form.filter_fields:
                    selected_values = cleaned_data[field_name]
                    if selected_values:
                        if field_name == 'computer_processor_frequency':
                            selected_ranges = {
                                label: (minimum, maximum)
                                for label, minimum, maximum in filter_form.frequency_ranges
                                if label in selected_values
                            }
                            matching_ids = []
                            for product_id, stored_value in context['products'].values_list(
                                'pk',
                                field_name,
                            ):
                                frequency = filter_form.parse_frequency(stored_value)
                                if frequency is not None and any(
                                    (minimum is None or frequency > minimum)
                                    and (maximum is None or frequency <= maximum)
                                    for minimum, maximum in selected_ranges.values()
                                ):
                                    matching_ids.append(product_id)
                            context['products'] = context['products'].filter(pk__in=matching_ids)
                        elif field_name in filter_form.multi_value_fields:
                            matching_values = Q()
                            for value in selected_values:
                                for alias in filter_form.filter_value_aliases(field_name, value):
                                    if field_name == 'video_card_connectors':
                                        matching_values |= Q(**{f'{field_name}__icontains': alias})
                                    else:
                                        matching_values |= (
                                            Q(**{f'{field_name}__iexact': alias})
                                            | Q(**{f'{field_name}__istartswith': f'{alias},'})
                                            | Q(**{f'{field_name}__icontains': f', {alias},'})
                                            | Q(**{f'{field_name}__icontains': f',{alias},'})
                                            | Q(**{f'{field_name}__iendswith': f', {alias}'})
                                            | Q(**{f'{field_name}__iendswith': f',{alias}'})
                                        )
                            context['products'] = context['products'].filter(matching_values)
                        else:
                            matching_values = Q()
                            for value in selected_values:
                                for alias in filter_form.filter_value_aliases(field_name, value):
                                    matching_values |= Q(**{f'{field_name}__iexact': alias})
                            context['products'] = context['products'].filter(matching_values)

            context['filter_form'] = filter_form
            context['filter_groups'] = filter_form.filter_groups
        return context


class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'

    video_card_specification_groups = (
        ('Основні характеристики', (
            'video_card_family',
            'video_card_form_factor',
            'video_card_purpose',
            'video_card_chip',
            'video_card_interface',
            'video_card_memory_capacity',
            'video_card_memory_type',
            'video_card_memory_bus',
            'video_card_boost_clock',
            'video_card_memory_frequency',
            'video_card_max_displays',
            'video_card_max_resolution',
            'video_card_hdcp',
            'video_card_connectors',
            'video_card_cooling_system',
            'video_card_cooling_type',
            'video_card_fan_count',
            'video_card_power_connectors',
            'video_card_recommended_psu',
            'video_card_directx',
            'video_card_opengl',
            'video_card_dlss',
            'video_card_dimensions',
            'video_card_weight',
        )),
        ('Інші', (
            'video_card_manufacturer',
            'video_card_country_of_origin',
            'video_card_warranty_months',
            'video_card_barcode',
            'video_card_note',
        )),
    )

    motherboard_specification_groups = (
        ('Основні характеристики', (
            'motherboard_purpose',
        )),
        ('Процесор', (
            'motherboard_product_socket',
            'motherboard_supported_processors',
        )),
        ('Слоти розширення', (
            'motherboard_expansion_slots',
        )),
        ('Чипсет', (
            'motherboard_chipset_model',
        )),
        ("Оперативна пам'ять", (
            'motherboard_ram_type',
            'motherboard_ram_slots',
            'motherboard_max_ram',
            'motherboard_ram_frequencies',
            'motherboard_dual_channel_support',
            'motherboard_ecc_support',
        )),
        ('Вбудована графіка', (
            'motherboard_integrated_video',
        )),
        ('Звук', (
            'motherboard_audio_controller',
            'motherboard_multichannel_audio',
        )),
        ("Провідний зв'язок", (
            'motherboard_lan_port_count',
            'motherboard_network_adapter',
            'motherboard_lan_speed',
            'motherboard_lan_speed',
        )),
        ("Порти і роз'єми на задній панелі", (
            'motherboard_rear_ports',
        )),
        ("Внутрішні роз'єми і колодки", (
            'motherboard_internal_ports',
            'motherboard_power_connector',
            'motherboard_headers',
            'motherboard_fan_headers',
            'motherboard_other_connectors',
        )),
        ('BIOS', (
            'motherboard_bios_type',
        )),
        ('Додатково', (
            'motherboard_raid_controller',
            'motherboard_search_tag',
            'motherboard_operating_system',
        )),
        ('Фізичні характеристики', (
            'motherboard_form_factor',
            'motherboard_height',
            'motherboard_width',
        )),
        ('Інші', (
            'motherboard_manufacturer',
            'motherboard_country_of_origin',
            'motherboard_warranty_months',
            'motherboard_barcode',
            'motherboard_note',
        )),
    )

    processor_specification_groups = (
        ('Основні технічні характеристики', (
            'cpu_family',
            'cpu_socket',
            'cpu_core_count',
            'cpu_thread_count',
            'cpu_base_clock',
            'cpu_max_clock',
            'cpu_tdp',
            'cpu_process_technology',
            'cpu_l1_cache',
            'cpu_l2_cache',
            'cpu_l3_cache',
        )),
        ("Пам'ять", (
            'cpu_max_memory',
            'cpu_memory_type',
            'cpu_max_memory_speed',
            'cpu_memory_channels',
        )),
        ('Відео', (
            'cpu_integrated_graphics',
        )),
        ('Додаткові характеристики', (
            'cpu_intel_generation',
            'cpu_amd_architecture',
            'cpu_max_temperature',
            'cpu_unlocked_multiplier',
            'cpu_pcie_version',
            'cpu_release_date',
            'cpu_package_type',
            'cpu_cooling_included',
        )),
        ('Інші', (
            'cpu_manufacturer',
            'cpu_country_of_origin',
            'cpu_warranty_months',
            'cpu_barcode',
            'cpu_note',
        )),
    )

    computer_specification_groups = (
        ('Основні характеристики', (
            'computer_type',
            'computer_view',
            'computer_display_diagonal',
            'computer_screen_type',
        )),
        ('Процесор', (
            'computer_intel_generation',
            'computer_amd_generation',
            'computer_processor_series',
            'computer_processor',
            'computer_processor_cores',
            'processor_threads',
            'computer_processor_frequency',
            'processor_boost_frequency',
            'processor_boost_supported',
        )),
        ('Материнська плата', (
            'motherboard_socket',
            'motherboard_chipset',
        )),
        ('Відеокарта', (
            'computer_graphics_type',
            'graphics_card_manufacturer',
            'computer_discrete_graphics_series',
            'computer_video_memory',
        )),
        ("Оперативна пам'ять", (
            'computer_ram_capacity',
            'ram_form_factor',
            'computer_ram_slots',
            'computer_ram_type',
            'computer_ram_frequency',
            'computer_ram_standard',
            'computer_ram_max_capacity',
        )),
        ('Система зберігання', (
            'computer_storage_types',
            'computer_ssd_capacity',
            'computer_hdd_capacity',
            'computer_optical_drive',
            'computer_card_reader',
        )),
        ('Мультимедіа', (
            'computer_built_in_microphone',
            'computer_webcam',
            'computer_built_in_speakers',
            'computer_audio_controller',
            'computer_multichannel_audio',
        )),
        ('Комунікаційні можливості', (
            'computer_wired_network',
            'computer_wireless_technologies',
        )),
        ('Порти та роз’єми', (
            'computer_interfaces',
        )),
        ('Програмне забезпечення', (
            'computer_operating_system',
        )),
        ('Додатково', (
            'computer_peripherals_included',
            'computer_additional_features',
            'computer_features',
            'computer_vesa_support',
            'computer_vr_support',
            'computer_backlit',
        )),
        ('Корпус', (
            'case_model',
            'case_metal_thickness',
            'case_material',
            'psu_location',
            'psu_power',
            'case_lighting',
            'cooling',
            'computer_width',
            'computer_height',
            'computer_depth',
            'computer_color',
        )),
        ('Інші характеристики', (
            'computer_manufacturer',
            'computer_country_of_origin',
            'computer_warranty_months',
            'computer_weight',
        )),
    )

    specification_groups = (
        ('Основні характеристики', (
            'manufacturer',
            'model_series',
            'laptop_type',
            'color',
        )),
        ('Дисплей', (
            'display_diagonal',
            'resolution',
            'matrix_type',
            'screen_surface',
            'refresh_rate',
        )),
        ('Процесор', (
            'intel_generation',
            'amd_generation',
            'processor',
            'processor_cores',
        )),
        ("Оперативна пам'ять", (
            'ram_type',
            'ram_capacity',
            'ram_slots',
        )),
        ('Система зберігання даних', (
            'ssd_capacity',
        )),
        ('Відеокарта', (
            'graphics_type',
            'discrete_graphics_series',
            'video_memory',
        )),
        ('Комунікації та інтерфейси', (
            'wireless_technologies',
            'interfaces',
        )),
        ('Мультимедіа та додаткові можливості', (
            'webcam',
            'additional_features',
            'features',
        )),
        ('Програмне забезпечення та живлення', (
            'operating_system',
            'battery_capacity',
        )),
        ('Корпус та гарантія', (
            'width',
            'height',
            'depth',
            'weight',
            'country_of_origin',
            'warranty_months',
        )),
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
        context['product_images'] = [
            {
                'url': image.image_url,
                'alt': image.alt_text or product.name,
            }
            for image in product.gallery_images.all()
        ]
        if product.image_url and all(
            image['url'] != product.image_url
            for image in context['product_images']
        ):
            context['product_images'].insert(0, {
                'url': product.image_url,
                'alt': product.name,
            })
        computer_category_name = (
            product.category.name.strip().casefold().replace("'", '’')
        )
        if (
            _is_computer_components_category(product.category)
            and product.component_type == 'processor'
        ):
            specification_groups = self.processor_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'graphics_card'
        ):
            specification_groups = self.video_card_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'motherboard'
        ):
            specification_groups = self.motherboard_specification_groups
        elif computer_category_name == 'комп’ютери':
            specification_groups = self.computer_specification_groups
        else:
            specification_groups = self.specification_groups
        context['specification_groups'] = [
            {
                'name': group_name,
                'items': [
                    (
                        product._meta.get_field(field_name).verbose_name,
                        getattr(product, field_name).strftime('%d.%m.%Y')
                        if field_name == 'cpu_release_date' and getattr(product, field_name)
                        else getattr(product, field_name),
                    )
                    for field_name in field_names
                    if getattr(product, field_name) not in (None, '')
                ],
            }
            for group_name, field_names in specification_groups
            if any(
                getattr(product, field_name) not in (None, '')
                for field_name in field_names
            )
        ]
        context['specifications'] = [
            item
            for group in context['specification_groups']
            for item in group['items']
        ]
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True,
        ).exclude(pk=product.pk)[:4]
        context['favorite_ids'] = _favorite_ids(self.request)
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

    initial = {}
    if request.user.is_authenticated:
        profile = getattr(request.user, 'customer_profile', None)
        initial = {
            'customer_name': ' '.join(
                name for name in (request.user.first_name, request.user.last_name) if name
            ) or request.user.username,
            'email': request.user.email,
            'phone': profile.phone if profile else '',
        }
    form = CheckoutForm(
        request.POST if request.method == 'POST' else None,
        initial=initial if request.method != 'POST' else None,
    )
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
                user=request.user if request.user.is_authenticated else None,
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
    if request.POST.get('next_url') == 'account_favorites':
        return redirect(f'{reverse_lazy("profile")}?section=favorites')
    next_url = request.POST.get('next_url', '')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        orders = user.store_orders.prefetch_related('items__product__category')
        section = self.request.GET.get('section', 'orders')
        if section not in ('orders', 'favorites', 'personal'):
            section = 'orders'
        order_status = self.request.GET.get('orders', 'all')
        if order_status == 'active':
            displayed_orders = orders.filter(status__in=('new', 'processing'))
        elif order_status in ('completed', 'cancelled'):
            displayed_orders = orders.filter(status=order_status)
        else:
            order_status = 'all'
            displayed_orders = orders
        favorite_ids = self.request.session.get('favorites', [])
        if not isinstance(favorite_ids, list):
            favorite_ids = []
        favorite_ids = [value for value in favorite_ids if str(value).isdigit()]
        context.update({
            'section': section,
            'profile_form': ProfileDetailsForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': profile.phone,
            }),
            'orders': displayed_orders,
            'order_status': order_status,
            'active_orders_count': orders.filter(status__in=('new', 'processing')).count(),
            'completed_orders_count': orders.filter(status='completed').count(),
            'cancelled_orders_count': orders.filter(status='cancelled').count(),
            'favorite_products': Product.objects.filter(
                pk__in=[int(value) for value in favorite_ids],
                is_active=True,
            ).select_related('category'),
            'favorites_count': len(favorite_ids),
            'cart_count': _cart_count(self.request),
            'categories': Category.objects.all(),
        })
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileDetailsForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save(update_fields=('first_name', 'last_name', 'email'))
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
            profile.phone = form.cleaned_data['phone']
            profile.save(update_fields=('phone',))
            messages.success(request, 'Персональні дані збережено.')
            return redirect(f'{reverse_lazy("profile")}?section=personal#personal-data')

        context = self.get_context_data(**kwargs)
        context['section'] = 'personal'
        context['profile_form'] = form
        return self.render_to_response(context, status=400)


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