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
    ComputerCaseProductFilterForm,
    ComputerProductFilterForm,
    CoolingProductFilterForm,
    HDDProductFilterForm,
    LaptopProductFilterForm,
    MemoryProductFilterForm,
    MonitorProductFilterForm,
    MotherboardProductFilterForm,
    NetworkProductFilterForm,
    PowerSupplyProductFilterForm,
    ProcessorProductFilterForm,
    ProductReviewForm,
    ProfileDetailsForm,
    RegistrationForm,
    SSDProductFilterForm,
    ThermalPasteProductFilterForm,
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


def _is_peripheral_category(category):
    return category.name.strip().casefold().replace("'", '’') == 'периферія'


def _is_thermal_paste_category_name(category_name):
    normalized_name = category_name.strip().casefold().replace("'", '’')
    return normalized_name in ('термопаста', 'термопасти', 'обслуговування пк')


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
                if _is_peripheral_category(category):
                    return redirect('peripheral_catalog', category_id=category.pk)
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
        context['categories'] = Category.objects.exclude(name='Аксесуари')
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
            'ssd',
            'SSD накопичувачі',
            'Швидке зберігання системи, програм і файлів',
            'https://brain.com.ua/static/images/prod_img/0/6/U0953606_1738404203.webp',
        ),
        (
            'hdd',
            'Жорсткі диски HDD',
            'Містке зберігання файлів і резервних копій',
            'https://brain.com.ua/static/images/prod_img/3/0/U0811330_1738963508.webp',
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


class PeripheralCatalogView(TemplateView):
    template_name = 'peripheral_catalog.html'

    peripheral_cards = (
        (
            'keyboard',
            'Клавіатури',
            'Клавіатури для роботи, навчання та ігор',
            'https://brain.com.ua/static/images/prod_img/9/7/B0005197_1740073227.webp',
        ),
        (
            'mouse',
            'Мишки',
            'Дротові та бездротові мишки',
            'https://brain.com.ua/static/images/prod_img/6/5/U0045165_1740076257.webp',
        ),
        (
            'mouse_pad',
            'Килимки',
            'Килимки для комфортного керування мишкою',
            'https://brain.com.ua/static/images/prod_img/2/5/U0720825_1739613411.webp',
        ),
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category,
            pk=self.kwargs['category_id'],
            name='Периферія',
        )
        counts = dict(
            Product.objects.filter(category=category, is_active=True)
            .values('peripheral_type')
            .annotate(product_count=Count('pk'))
            .values_list('peripheral_type', 'product_count')
        )
        context.update({
            'category': category,
            'categories': Category.objects.all(),
            'cart_count': _cart_count(self.request),
            'peripheral_cards': [
                {
                    'type': peripheral_type,
                    'title': title,
                    'description': description,
                    'image_url': image_url,
                    'product_count': counts.get(peripheral_type, 0),
                }
                for peripheral_type, title, description, image_url in self.peripheral_cards
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
        if _is_peripheral_category(category):
            peripheral_type = request.GET.get('peripheral_type')
            valid_types = {value for value, _ in Product.PERIPHERAL_TYPE_CHOICES}
            if peripheral_type not in valid_types:
                return redirect('peripheral_catalog', category_id=category.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        context['categories'] = Category.objects.all()
        context['cart_count'] = _cart_count(self.request)
        context['favorite_ids'] = _favorite_ids(self.request)
        context['category'] = category
        context['category_title'] = (
            'Ноутбуки'
            if category.name.strip().casefold().startswith('ноутбук')
            else category.name
        )
        context['thermal_paste_catalog'] = _is_thermal_paste_category_name(category.name)
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
            context['memory_catalog'] = selected_type == 'memory'
            context['ssd_catalog'] = selected_type == 'ssd'
            context['hdd_catalog'] = selected_type == 'hdd'
            context['case_catalog'] = selected_type == 'case'
            context['power_supply_catalog'] = selected_type == 'power_supply'
            context['cooling_catalog'] = selected_type == 'cooling'
        if _is_peripheral_category(category):
            selected_type = self.request.GET['peripheral_type']
            selected_title = dict(Product.PERIPHERAL_TYPE_CHOICES)[selected_type]
            context['products'] = context['products'].filter(peripheral_type=selected_type)
            context['category_title'] = selected_title
            context['peripheral_category'] = True
            context['selected_peripheral_type'] = selected_type
        context['filter_groups'] = ()
        context['filter_form'] = None
        context['placeholder_filter_groups'] = ()
        normalized_category_name = category.name.strip().casefold().replace("'", '’')
        filter_form_class = None
        if normalized_category_name.startswith('ноутбук'):
            filter_form_class = LaptopProductFilterForm
        elif normalized_category_name == 'комп’ютери':
            filter_form_class = ComputerProductFilterForm
        elif normalized_category_name == 'монітори':
            filter_form_class = MonitorProductFilterForm
        elif normalized_category_name == 'мережеві фільтри та подовжувачі':
            filter_form_class = NetworkProductFilterForm
        elif _is_thermal_paste_category_name(category.name):
            filter_form_class = ThermalPasteProductFilterForm
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
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'memory'
        ):
            filter_form_class = MemoryProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'ssd'
        ):
            filter_form_class = SSDProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'hdd'
        ):
            filter_form_class = HDDProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'case'
        ):
            filter_form_class = ComputerCaseProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'power_supply'
        ):
            filter_form_class = PowerSupplyProductFilterForm
        elif (
            _is_computer_components_category(category)
            and self.request.GET.get('component_type') == 'cooling'
        ):
            filter_form_class = CoolingProductFilterForm

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
                        elif field_name in getattr(filter_form, 'range_filter_fields', {}):
                            selected_ranges = {
                                label: (minimum, maximum)
                                for label, minimum, maximum
                                in filter_form.range_filter_fields[field_name]
                                if label in selected_values
                            }
                            matching_ids = []
                            for product_id, stored_value in context['products'].values_list(
                                'pk',
                                field_name,
                            ):
                                speed = filter_form.parse_speed(stored_value)
                                if speed is not None and any(
                                    speed >= minimum
                                    and (maximum is None or speed <= maximum)
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

    thermal_paste_specification_groups = (
        ('Основні характеристики', (
            'thermal_compatibility',
            'thermal_conductivity',
            'thermal_weight',
            'thermal_packaging',
        )),
        ('Інші', (
            'thermal_manufacturer',
            'thermal_country_of_origin',
            'thermal_barcode',
            'thermal_note',
        )),
    )

    thermal_paste_specification_labels = {
        'thermal_compatibility': 'Сумісність',
        'thermal_conductivity': 'Теплопровідність',
        'thermal_weight': 'Вага',
        'thermal_packaging': 'Тип упаковки',
        'thermal_manufacturer': 'Виробник',
        'thermal_country_of_origin': 'Країна виробництва',
        'thermal_barcode': 'Штрихкод',
        'thermal_note': 'Примітка',
    }

    network_specification_groups = (
        ('Основні характеристики', (
            'network_product_type',
            'network_socket_count',
            'network_outlet_type',
            'network_input_plug_type',
            'network_usb_ports',
            'network_cable_length',
            'network_cable_specification',
            'network_filter_material',
            'network_features',
            'network_additional_features',
            'network_nominal_voltage',
            'network_protection',
            'network_total_power',
            'network_breaker_trip_current',
            'color',
            'manufacturer',
            'country_of_origin',
            'warranty_months',
            'network_barcode',
            'network_note',
            'features',
        )),
    )

    network_specification_labels = {
        'network_product_type': 'Тип',
        'network_socket_count': 'Кількість розеток',
        'network_outlet_type': 'Тип вихідних розеток',
        'network_input_plug_type': 'Тип вхідної вилки',
        'network_usb_ports': 'USB-порти',
        'network_cable_length': 'Довжина кабелю',
        'network_cable_specification': 'Технічні характеристики кабелю',
        'network_filter_material': 'Матеріал фільтра',
        'network_features': 'Особливості',
        'network_additional_features': 'Додаткові характеристики',
        'network_nominal_voltage': 'Номінальна напруга',
        'network_protection': 'Захист',
        'network_total_power': 'Сумарна потужність підключеного навантаження',
        'network_breaker_trip_current': 'Струм спрацьовування термозапобіжника',
        'manufacturer': 'Виробник',
        'country_of_origin': 'Країна виробництва',
        'warranty_months': 'Гарантія, міс',
        'network_barcode': 'Штрихкод',
        'network_note': 'Примітка',
    }

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

    memory_specification_groups = (
        ('Основні характеристики', (
            'memory_type',
            'memory_capacity',
            'memory_module_count',
            'memory_frequency',
            'memory_standard',
            'memory_timing',
            'memory_voltage',
            'memory_cooling',
            'memory_lighting',
            'memory_form_factor',
            'memory_ecc',
            'memory_buffering',
        )),
        ('Додатково', (
            'memory_additional_note',
        )),
        ('Інші', (
            'memory_manufacturer',
            'memory_country_of_origin',
            'memory_warranty_months',
            'memory_barcode',
            'memory_note',
        )),
    )

    ssd_specification_groups = (
        ('Основні характеристики', (
            'ssd_drive_type',
            'model_series',
            'ssd_component_capacity',
            'ssd_flash_type',
            'ssd_form_factor',
            'ssd_m2_size',
            'ssd_interface',
            'ssd_read_speed',
            'ssd_write_speed',
        )),
        ('Додатково', (
            'ssd_endurance',
            'ssd_tbw',
            'ssd_power_consumption',
        )),
        ('Фізичні характеристики', (
            'ssd_dimensions',
            'ssd_thickness',
            'ssd_weight',
            'ssd_color',
        )),
        ('Інші', (
            'ssd_manufacturer',
            'ssd_country_of_origin',
            'ssd_warranty_months',
            'ssd_barcode',
            'ssd_note',
        )),
    )

    hdd_specification_groups = (
        ('Основні характеристики', (
            'hdd_drive_type',
            'hdd_component_capacity',
            'hdd_rpm',
            'hdd_buffer_size',
            'hdd_interface',
            'hdd_form_factor',
            'hdd_series',
        )),
        ('Інші', (
            'hdd_manufacturer',
            'hdd_country_of_origin',
            'hdd_warranty_months',
            'hdd_barcode',
            'hdd_note',
        )),
    )

    hdd_specification_labels = {
        'hdd_drive_type': 'Тип',
        'hdd_component_capacity': 'Об’єм',
        'hdd_rpm': 'Швидкість обертання шпинделя',
        'hdd_buffer_size': 'Розмір буфера',
        'hdd_interface': 'Інтерфейс',
        'hdd_form_factor': 'Форм-фактор',
        'hdd_series': 'Лінійка (Серія)',
        'hdd_manufacturer': 'Виробник',
        'hdd_country_of_origin': 'Країна виробництва',
        'hdd_warranty_months': 'Гарантія, міс',
        'hdd_barcode': 'Штрихкод',
        'hdd_note': 'Примітка',
    }

    case_specification_groups = (
        ('Основні характеристики', (
            'case_class',
            'case_form_factor',
            'case_installation',
            'case_supported_motherboards',
            'case_psu_included',
            'psu_location',
        )),
        ('Зовнішні відсіки', (
            'case_external_bays_5_25',
            'case_external_bays_3_5',
        )),
        ('Внутрішні відсіки', (
            'case_internal_bays_5_25',
            'case_3_5_bays',
            'case_internal_bays_2_5',
        )),
        ('Слоти розширення', (
            'case_expansion_slots',
        )),
        ('Охолодження', (
            'case_fan_configuration',
            'case_additional_fan_positions',
            'case_cooling_elements',
            'case_dust_filter',
            'case_liquid_cooling_support',
            'case_max_noise',
        )),
        ('Функції та можливості', (
            'case_external_connectors',
            'computer_additional_features',
            'case_gpu_clearance',
            'case_cpu_cooler_clearance',
            'case_lighting',
            'case_material',
        )),
        ('Фізичні характеристики', (
            'case_dimensions',
            'case_weight',
            'case_color',
        )),
        ('Інші', (
            'case_manufacturer',
            'case_country_of_origin',
            'case_warranty_months',
            'case_barcode',
            'case_note',
        )),
    )

    case_specification_labels = {
        'case_class': 'Клас корпусу',
        'case_form_factor': 'Типорозмір',
        'case_installation': 'Спосіб установки',
        'case_supported_motherboards': 'Підтримувані материнські плати',
        'case_psu_included': 'Наявність блоку живлення',
        'psu_location': 'Розташування блоку живлення',
        'case_external_bays_5_25': 'Кількість зовнішніх відсіків 5.25"',
        'case_external_bays_3_5': 'Кількість зовнішніх відсіків 3.5"',
        'case_internal_bays_5_25': 'Кількість внутрішніх відсіків 5.25"',
        'case_3_5_bays': 'Кількість внутрішніх відсіків 3.5"',
        'case_internal_bays_2_5': 'Кількість внутрішніх відсіків 2.5"',
        'case_expansion_slots': 'Кількість слотів розширення',
        'case_fan_configuration': 'Кількість і розмір встановлених вентиляторів',
        'case_additional_fan_positions': 'Місця для додаткових вентиляторів',
        'case_cooling_elements': 'Охолоджуючі елементи',
        'case_dust_filter': 'Пиловий фільтр',
        'case_liquid_cooling_support': 'Підтримка рідинного охолодження',
        'case_max_noise': 'Максимальний рівень шуму',
        'case_external_connectors': 'Зовнішні роз’єми',
        'computer_additional_features': 'Особливості',
        'case_gpu_clearance': 'Встановлення довгих відеокарт',
        'case_cpu_cooler_clearance': 'Максимальна висота процесорного кулера',
        'case_lighting': 'Наявність підсвічування',
        'case_material': 'Матеріал корпусу',
        'case_dimensions': 'Розмір, мм',
        'case_weight': 'Вага, кг',
        'case_color': 'Колір',
        'case_manufacturer': 'Виробник',
        'case_country_of_origin': 'Країна виробництва',
        'case_warranty_months': 'Гарантія, міс',
        'case_barcode': 'Штрихкод',
        'case_note': 'Примітка',
    }

    power_supply_specification_groups = (
        ('Основні характеристики', (
            'psu_type',
            'psu_standard',
            'psu_wattage',
            'psu_modular_connection',
            'psu_certification',
            'psu_pfc',
            'psu_motherboard_connector',
            'psu_cpu_connector',
            'psu_gpu_connector',
            'psu_pcie_connectors',
            'psu_sata_connectors',
            'psu_peripheral_connectors',
            'psu_output_current_5v',
            'psu_output_current_3_3v',
            'psu_output_current_12v',
            'psu_output_current_minus_12v',
            'psu_output_current_5vsb',
            'psu_cooling_type',
            'psu_fan_diameter',
            'psu_protection',
            'psu_dimensions',
        )),
        ('Інші', (
            'psu_manufacturer',
            'psu_country_of_origin',
            'psu_warranty_months',
            'psu_barcode',
            'features',
        )),
    )

    power_supply_specification_labels = {
        'psu_type': 'Тип БЖ',
        'psu_standard': 'Стандарт БЖ',
        'psu_wattage': 'Потужність',
        'psu_modular_connection': 'Модульне підключення кабелів',
        'psu_certification': 'Сертифікація 80 PLUS',
        'psu_pfc': 'Модуль PFC',
        'psu_motherboard_connector': 'Підключення материнської плати',
        'psu_cpu_connector': 'Підключення процесора',
        'psu_gpu_connector': 'Підключення відеокарти',
        'psu_pcie_connectors': 'Кіль-ть роз’ємів додаткового живлення для відеокарт',
        'psu_sata_connectors': 'Кількість роз’ємів SATA',
        'psu_peripheral_connectors': 'Кількість роз’ємів Peripheral',
        'psu_output_current_5v': 'Output Current +5V',
        'psu_output_current_3_3v': 'Output Current +3,3V',
        'psu_output_current_12v': 'Output Current +12V',
        'psu_output_current_minus_12v': 'Output Current -12V',
        'psu_output_current_5vsb': 'Output Current +5Vsb',
        'psu_cooling_type': 'Тип охолодження',
        'psu_fan_diameter': 'Діаметр вентиляторів',
        'psu_protection': 'Захист від',
        'psu_dimensions': 'Розмір, мм',
        'psu_manufacturer': 'Виробник',
        'psu_country_of_origin': 'Країна виробництва',
        'psu_warranty_months': 'Гарантія, міс',
        'psu_barcode': 'Штрихкод',
        'features': 'Примітка',
    }

    cooling_specification_groups = (
        ('Основні характеристики', (
            'cooling_cpu_compatibility',
            'cooling_socket',
            'cooling_fan_count',
            'cooling_fan_diameter',
            'cooling_lighting',
            'cooling_max_fan_speed',
        )),
        ('Додаткові характеристики', (
            'cooling_radiator_material',
            'cooling_airflow',
            'cooling_fan_speed_control',
            'cooling_pump_power_connector',
            'cooling_fan_power_connector',
            'cooling_pump_voltage',
            'cooling_tube_length',
            'cooling_max_tdp',
            'cooling_noise_level',
        )),
        ('Фізичні характеристики', (
            'cooling_radiator_dimensions',
            'cooling_fan_dimensions',
            'cooling_pump_dimensions',
            'cooling_color',
        )),
        ('Інші', (
            'cooling_manufacturer',
            'cooling_country_of_origin',
            'cooling_warranty_months',
            'cooling_barcode',
            'cooling_note',
        )),
    )

    monitor_specification_groups = (
        ('Основні характеристики', (
            'monitor_display_type',
            'display_diagonal',
            'matrix_type',
            'resolution',
            'refresh_rate',
            'monitor_aspect_ratio',
            'monitor_backlight',
            'screen_surface',
            'monitor_response_time',
            'monitor_brightness',
            'monitor_static_contrast',
            'monitor_dynamic_contrast',
            'monitor_viewing_angles',
            'monitor_max_colors',
            'monitor_image_enhancement',
            'monitor_sync_technology',
        )),
        ('Роз’єми й інтерфейси', (
            'interfaces',
        )),
        ('Електричні параметри', (
            'monitor_power_consumption',
            'monitor_standby_power',
        )),
        ('Додатково', (
            'monitor_stand_adjustment',
            'monitor_tilt_angle',
            'monitor_vesa',
            'built_in_speakers',
        )),
        ('Фізичні характеристики', (
            'monitor_dimensions_with_stand',
            'monitor_dimensions_without_stand',
            'monitor_weight_unboxed',
            'monitor_weight_boxed',
            'color',
        )),
        ('Інші', (
            'manufacturer',
            'country_of_origin',
            'warranty_months',
            'features',
        )),
    )

    monitor_specification_labels = {
        'monitor_display_type': 'Тип монітора',
        'display_diagonal': 'Діагональ екрана',
        'matrix_type': 'Тип матриці',
        'resolution': 'Роздільна здатність',
        'refresh_rate': 'Частота оновлення екрану',
        'monitor_aspect_ratio': 'Співвідношення сторін',
        'monitor_backlight': 'Підсвічування',
        'screen_surface': 'Покриття екрана',
        'monitor_response_time': 'Час реакції матриці',
        'monitor_brightness': 'Яскравість',
        'monitor_static_contrast': 'Контрастність статична',
        'monitor_dynamic_contrast': 'Контрастність динамічна',
        'monitor_viewing_angles': 'Кути огляду (гориз./вертик.)',
        'monitor_max_colors': 'Максимальна кількість кольорів',
        'monitor_image_enhancement': 'Технології покращення зображення',
        'monitor_sync_technology': 'Технології синхронізації',
        'interfaces': 'Інтерфейси та підключення',
        'monitor_power_consumption': 'Споживана потужність у робочому режимі',
        'monitor_standby_power': 'Споживана потужність у режимі очікування',
        'monitor_stand_adjustment': 'Регулювання положення',
        'monitor_tilt_angle': 'Регулювання нахилу',
        'monitor_vesa': 'VESA',
        'built_in_speakers': 'Вбудовані колонки',
        'monitor_dimensions_with_stand': 'Розміри з підставкою',
        'monitor_dimensions_without_stand': 'Розміри без підставки',
        'monitor_weight_unboxed': 'Вага без упаковки',
        'monitor_weight_boxed': 'Вага з упаковкою',
        'color': 'Колір',
        'manufacturer': 'Виробник',
        'country_of_origin': 'Країна виробництва',
        'warranty_months': 'Гарантія, міс',
        'features': 'Примітка',
    }

    cooling_specification_labels = {
        'cooling_cpu_compatibility': 'Для процесорів',
        'cooling_socket': 'Сокет',
        'cooling_fan_count': 'Кількість вентиляторів',
        'cooling_fan_diameter': 'Діаметр вентиляторів',
        'cooling_lighting': 'Підсвічування',
        'cooling_max_fan_speed': 'Максимальна частота обертів',
        'cooling_radiator_material': 'Матеріал радіатора',
        'cooling_airflow': 'Повітряний потік',
        'cooling_fan_speed_control': 'Управління швидкістю обертання',
        'cooling_pump_power_connector': 'Роз’єм живлення помпи',
        'cooling_fan_power_connector': 'Роз’єм живлення вентиляторів',
        'cooling_pump_voltage': 'Напруга живлення',
        'cooling_tube_length': 'Довжина патрубків',
        'cooling_max_tdp': 'Максимальний TDP',
        'cooling_noise_level': 'Рівень шуму',
        'cooling_radiator_dimensions': 'Розміри радіатора',
        'cooling_fan_dimensions': 'Розміри вентиляторів',
        'cooling_pump_dimensions': 'Розмір водоблоку',
        'cooling_color': 'Колір',
        'cooling_manufacturer': 'Виробник',
        'cooling_country_of_origin': 'Країна виробництва',
        'cooling_warranty_months': 'Гарантія, міс',
        'cooling_barcode': 'Штрихкод',
        'cooling_note': 'Примітка',
    }

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
            and product.component_type == 'memory'
        ):
            specification_groups = self.memory_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'ssd'
        ):
            specification_groups = self.ssd_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'hdd'
        ):
            specification_groups = self.hdd_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'case'
        ):
            specification_groups = self.case_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'power_supply'
        ):
            specification_groups = self.power_supply_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'cooling'
        ):
            specification_groups = self.cooling_specification_groups
        elif (
            _is_computer_components_category(product.category)
            and product.component_type == 'motherboard'
        ):
            specification_groups = self.motherboard_specification_groups
        elif computer_category_name == 'монітори':
            specification_groups = self.monitor_specification_groups
        elif computer_category_name == 'мережеві фільтри та подовжувачі':
            specification_groups = self.network_specification_groups
        elif _is_thermal_paste_category_name(product.category.name):
            specification_groups = self.thermal_paste_specification_groups
        elif computer_category_name == 'комп’ютери':
            specification_groups = self.computer_specification_groups
        else:
            specification_groups = self.specification_groups

        def specification_value(field_name):
            value = getattr(product, field_name)
            if product.component_type == 'power_supply':
                legacy_fields = {
                    'psu_manufacturer': 'manufacturer',
                    'psu_country_of_origin': 'country_of_origin',
                    'psu_warranty_months': 'warranty_months',
                }
                if field_name in legacy_fields and not value:
                    return getattr(product, legacy_fields[field_name])
            if product.component_type == 'cooling':
                legacy_fields = {
                    'cooling_manufacturer': 'manufacturer',
                    'cooling_country_of_origin': 'country_of_origin',
                    'cooling_warranty_months': 'warranty_months',
                    'cooling_note': 'features',
                }
                if field_name in legacy_fields and not value:
                    return getattr(product, legacy_fields[field_name])
            if (
                field_name == 'ssd_component_capacity'
                and not value
                and product.component_type == 'ssd'
            ):
                return product.ssd_capacity
            if product.component_type == 'hdd':
                legacy_fields = {
                    'hdd_component_capacity': 'hdd_capacity',
                    'hdd_manufacturer': 'manufacturer',
                    'hdd_series': 'model_series',
                    'hdd_country_of_origin': 'country_of_origin',
                    'hdd_warranty_months': 'warranty_months',
                    'hdd_note': 'features',
                }
                if field_name in legacy_fields and not value:
                    return getattr(product, legacy_fields[field_name])
            return value

        if computer_category_name == 'монітори':
            specification_labels = self.monitor_specification_labels
        elif computer_category_name == 'мережеві фільтри та подовжувачі':
            specification_labels = self.network_specification_labels
        elif _is_thermal_paste_category_name(product.category.name):
            specification_labels = self.thermal_paste_specification_labels
        elif product.component_type == 'hdd':
            specification_labels = self.hdd_specification_labels
        elif product.component_type == 'case':
            specification_labels = self.case_specification_labels
        elif product.component_type == 'power_supply':
            specification_labels = self.power_supply_specification_labels
        elif product.component_type == 'cooling':
            specification_labels = self.cooling_specification_labels
        else:
            specification_labels = {}

        context['specification_groups'] = [
            {
                'name': group_name,
                'items': [
                    (
                        specification_labels.get(
                            field_name,
                            product._meta.get_field(field_name).verbose_name,
                        ),
                        specification_value(field_name).strftime('%d.%m.%Y')
                        if field_name == 'cpu_release_date' and specification_value(field_name)
                        else specification_value(field_name),
                    )
                    for field_name in field_names
                    if specification_value(field_name) not in (None, '')
                ],
            }
            for group_name, field_names in specification_groups
            if any(
                specification_value(field_name) not in (None, '')
                for field_name in field_names
            )
        ]
        context['specifications'] = [
            item
            for group in context['specification_groups']
            for item in group['items']
        ]
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True,
        )
        if _is_computer_components_category(product.category) and product.component_type:
            related_products = related_products.filter(component_type=product.component_type)
        context['related_products'] = related_products.exclude(pk=product.pk)[:4]
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