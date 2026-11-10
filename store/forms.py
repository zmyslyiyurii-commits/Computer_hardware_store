from collections import Counter
from decimal import Decimal, InvalidOperation
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Count, Max, Min


class RegistrationForm(UserCreationForm):
    # Додаємо до стандартної форми Django обов'язкові прізвище та email.
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


class ProductReviewForm(forms.Form):
    author_name = forms.CharField(label="Ім'я", max_length=100)
    rating = forms.ChoiceField(
        label='Оцінка',
        choices=tuple((value, f'{value} зірок') for value in range(1, 6)),
        widget=forms.RadioSelect,
    )
    text = forms.CharField(
        label='Відгук',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Поділися враженнями про товар'}),
        min_length=5,
        max_length=2000,
    )


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(label="Ім'я та прізвище", max_length=150)
    phone = forms.CharField(label='Телефон', max_length=30)
    email = forms.EmailField(label='Електронна пошта')
    delivery_address = forms.CharField(label='Адреса доставки', max_length=255)


class ProfileDetailsForm(forms.Form):
    first_name = forms.CharField(label="Ім'я", max_length=150, required=False)
    last_name = forms.CharField(label='Прізвище', max_length=150, required=False)
    email = forms.EmailField(label='Електронна пошта', required=False)
    phone = forms.CharField(label='Телефон', max_length=30, required=False)


class LaptopProductFilterForm(forms.Form):
    price_min = forms.DecimalField(
        label='Від',
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'min': '0', 'step': '1', 'placeholder': 'від'}),
    )
    price_max = forms.DecimalField(
        label='До',
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'min': '0', 'step': '1', 'placeholder': 'до'}),
    )

    filter_fields = (
        ('manufacturer', 'Виробник'),
        ('model_series', 'Серія (модельний ряд)'),
        ('laptop_type', 'Тип ноутбуку'),
        ('display_diagonal', 'Діагональ дисплея'),
        ('resolution', 'Роздільна здатність'),
        ('matrix_type', 'Тип матриці'),
        ('screen_surface', 'Поверхня екрану'),
        ('refresh_rate', 'Частота оновлення екрану'),
        ('intel_generation', 'Покоління процесора Intel'),
        ('amd_generation', 'Покоління процесора AMD'),
        ('processor', 'Процесор'),
        ('processor_cores', 'Кількість ядер процесора'),
        ('ram_type', "Тип оперативної пам'яті"),
        ('ram_capacity', "Об'єм оперативної пам'яті"),
        ('ram_slots', "Кількість слотів для оперативної пам'яті"),
        ('ssd_capacity', 'Об’єм SSD'),
        ('graphics_type', 'Тип відеокарти'),
        ('discrete_graphics_series', 'Серія дискретної відеокарти'),
        ('video_memory', 'Об’єм відеопам’яті'),
        ('wireless_technologies', 'Бездротові технології'),
        ('interfaces', 'Інтерфейси та підключення'),
        ('operating_system', 'Операційна система'),
        ('battery_capacity', 'Ємність акумулятора'),
        ('features', 'Особливості'),
        ('weight', 'Вага'),
        ('color', 'Колір'),
    )

    multi_value_fields = ('wireless_technologies', 'interfaces', 'features')

    preset_options = {
        'model_series': (),
        'manufacturer': (
            'Acer',
            'AGN',
            'Apple',
            'ASUS',
            'Dell',
            'Dream Machines',
            'Geekom',
            'GIGABYTE',
            'HP',
            'Lenovo',
            'MSI',
            'Pixus',
            'Thunderobot',
            'Vinga',
        ),
        'laptop_type': (
            'бізнес',
            'для навчання',
            'для роботи',
            'захищений',
            'портативний',
            'трансформер',
            'ігровий',
            'нетбук',
        ),
        'display_diagonal': ('9" - 12.5"', '13"', '14"', '15" - 16"', '17"', '18" і більше'),
        'resolution': ('HD', 'Full HD', '2K', '3K', '4K'),
        'matrix_type': ('IPS', 'LCD', 'Mini LED', 'OLED', 'SVA', 'TN+film', 'UWVA', 'VA', 'WVA'),
        'screen_surface': ('антиблікове покриття', 'глянсова', 'матова'),
        'refresh_rate': ('60 Гц', '120 Гц', '144 Гц', '165 Гц', '180 Гц', '240 Гц', '250 Гц', '300 Гц'),
        'intel_generation': (
            '12-е покоління',
            '13-е покоління',
            '14-е покоління',
            '15-е покоління',
            '16-е покоління',
        ),
        'amd_generation': ('Zen 2', 'Zen 3', 'Zen 3+', 'Zen 4', 'Zen 5'),
        'processor': (
            'Intel Core Ultra 9',
            'Intel Core Ultra 7',
            'Intel Core Ultra 5',
            'Intel Core 9',
            'Intel Core 7',
            'Intel Core 5',
            'Intel Core 3',
            'Apple M5',
            'Apple A8',
            'Intel Core i9',
            'Intel Core i7',
            'Intel Core i5',
            'Intel Core i3',
            'AMD Ryzen AI Max',
            'AMD Ryzen AI 9',
            'AMD Ryzen AI 7',
            'AMD Ryzen AI 5',
            'AMD Ryzen 9',
            'AMD Ryzen 7',
            'AMD Ryzen 5',
            'AMD Ryzen 3',
            'Intel Pentium',
            'Intel Celeron',
            'Snapdragon',
            'Cortex',
        ),
        'processor_cores': ('4', '5', '6', '8', '10', '12', '14', '15', '16', '18', '20', '24'),
        'ram_type': ('DDR4', 'DDR5'),
        'ram_capacity': ('8 ГБ', '12 ГБ', '16 ГБ', '24 ГБ', '32 ГБ', '36 ГБ', '64 ГБ', '128 ГБ'),
        'ram_slots': ('відсутні, розпаяна на МП', '1', '2', '4'),
        'ssd_capacity': ('64 ГБ і менше', '256 ГБ', '512 ГБ', '1 ТБ', '2 ТБ', '4 ТБ і більше'),
        'graphics_type': ('дискретна', 'інтегрована'),
        'discrete_graphics_series': (
            'NVIDIA GeForce RTX 5090',
            'NVIDIA GeForce RTX 5080',
            'NVIDIA GeForce RTX 5070 Ti',
            'NVIDIA GeForce RTX 5070',
            'NVIDIA GeForce RTX 5060',
            'NVIDIA GeForce RTX 5050',
            'NVIDIA GeForce RTX 4050',
            'NVIDIA GeForce RTX 3050',
            'NVIDIA GeForce RTX 2050',
            'NVIDIA RTX PRO 5000',
            'NVIDIA RTX PRO 4000',
            'NVIDIA RTX PRO 2000',
            'NVIDIA RTX PRO 1000',
            'NVIDIA RTX PRO 500',
            'NVIDIA RTX 500 Ada',
            'AMD Radeon RX 6550M',
        ),
        'video_memory': ('4 ГБ', '6 ГБ', '8 ГБ', '12 ГБ', '16 ГБ', '24 ГБ'),
        'wireless_technologies': ('4G', 'Bluetooth', 'NFC', 'Wi-Fi'),
        'interfaces': (
            'USB Type-A',
            'USB Type-C',
            'Thunderbolt',
            'LAN (RJ-45)',
            'HDMI',
            'DisplayPort',
            'аудіо',
            'Smart Card',
        ),
        'operating_system': (
            'без операційної системи',
            'Linux',
            'Mac OS',
            'Windows 11 Home',
            'Windows 11 Pro',
            'Chrome OS',
        ),
        'battery_capacity': (
            '31 - 50 Вт-год',
            '51 - 70 Вт-год',
            '71 - 90 Вт-год',
            '91 Вт-год і більше',
        ),
        'features': (
            'GPS',
            'TPM модуль',
            'гніздо для замка Kensington',
            'з двома екранами',
            'зарядка від USB',
            'клавіатура - латиниця',
        ),
        'weight': (
            'менше 1.0 кг',
            '1.0 кг - 1.5 кг',
            '1.6 кг - 2.0 кг',
            '2.1 кг - 2.5 кг',
            '2.6 кг - 3.0 кг',
            '3.1 кг - 3.5 кг',
            'більше 3.5 кг',
        ),
        'color': (
            'бежевий',
            'блакитний',
            'білий',
            'бірюзовий',
            'жовтий',
            'зелений',
            'золотий',
            'рожевий',
            'синій',
            'сріблястий',
            'сірий',
            'чорний',
            'індіго',
        ),
    }

    def __init__(self, *args, products, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_groups = []

        price_range = products.aggregate(minimum=Min('price'), maximum=Max('price'))
        self.fields['price_min'].initial = price_range['minimum']
        self.fields['price_max'].initial = price_range['maximum']

        # Показуємо типові варіанти з каталогу та актуальні значення товарів.
        for field_name, label in self.filter_fields:
            if field_name in self.multi_value_fields:
                counts = Counter()
                for stored_values in products.values_list(field_name, flat=True):
                    counts.update({
                        self.normalize_filter_value(field_name, value)
                        for value in stored_values.split(',')
                        if value.strip()
                    })
            else:
                options = (
                    products.order_by()
                    .values(field_name)
                    .annotate(product_count=Count('pk'))
                    .exclude(**{field_name: ''})
                    .order_by(field_name)
                )
                counts = Counter()
                for option in options:
                    value = self.normalize_filter_value(field_name, option[field_name])
                    counts[value] += option['product_count']
            choices_by_key = {}
            for value in self.preset_options[field_name]:
                normalized_value = self.normalize_filter_value(field_name, value)
                choices_by_key.setdefault(normalized_value.casefold(), normalized_value)
            for value in sorted(counts, key=str.casefold):
                choices_by_key.setdefault(value.casefold(), value)
            choices = [
                (
                    value,
                    f'{value} ({counts[value]})' if counts.get(value, 0) else value,
                )
                for value in choices_by_key.values()
            ]
            self.fields[field_name] = forms.MultipleChoiceField(
                label=label,
                required=False,
                choices=choices,
                widget=forms.CheckboxSelectMultiple,
            )
            self.filter_groups.append({
                'name': label,
                'field': self[field_name],
            })

    def normalize_filter_value(self, field_name, value):
        return value.strip()

    def filter_value_aliases(self, field_name, value):
        return (value,)

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')

        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValidationError('Мінімальна ціна не може бути більшою за максимальну.')

        return cleaned_data


class ComputerProductFilterForm(LaptopProductFilterForm):
    frequency_ranges = (
        ('до 2 ГГц', None, Decimal('2')),
        ('2–2.5 ГГц', Decimal('2'), Decimal('2.5')),
        ('2.5–3 ГГц', Decimal('2.5'), Decimal('3')),
        ('3–3.5 ГГц', Decimal('3'), Decimal('3.5')),
        ('понад 3.5 ГГц', Decimal('3.5'), None),
    )

    @staticmethod
    def parse_frequency(value):
        match = re.search(r'\d+(?:[.,]\d+)?', value or '')
        if not match:
            return None
        try:
            return Decimal(match.group().replace(',', '.'))
        except InvalidOperation:
            return None

    filter_fields = (
        ('computer_manufacturer', 'Виробник'),
        ('computer_type', 'Тип ПК'),
        ('computer_view', 'Вид'),
        ('computer_display_diagonal', 'Діагональ екрану'),
        ('computer_screen_type', 'Тип екрану'),
        ('computer_processor_series', 'Серія процесора'),
        ('computer_amd_generation', 'Покоління процесора AMD'),
        ('computer_intel_generation', 'Покоління процесора Intel'),
        ('computer_processor_cores', 'Кількість ядер'),
        ('computer_processor_frequency', 'Частота процесора, ГГц'),
        ('computer_graphics_type', 'Тип відеокарти'),
        ('computer_discrete_graphics_series', 'Модель відеокарти'),
        ('computer_video_memory', "Об'єм графічної пам'яті"),
        ('computer_ram_capacity', "Об'єм оперативної пам'яті"),
        ('computer_ram_type', "Тип пам'яті"),
        ('computer_storage_types', 'Типи внутрішніх накопичувачів'),
        ('computer_hdd_capacity', 'Об’єм HDD'),
        ('computer_ssd_capacity', 'Об’єм SSD'),
        ('computer_optical_drive', 'Оптичний привід'),
        ('computer_card_reader', 'Кардридер'),
        ('computer_built_in_microphone', 'Вбудований мікрофон'),
        ('computer_webcam', 'Вбудована веб-камера'),
        ('computer_built_in_speakers', 'Вбудовані динаміки'),
        ('computer_wireless_technologies', "Бездротовий зв'язок"),
        ('computer_interfaces', 'Зовнішні порти та роз’єми'),
        ('computer_operating_system', 'Операційна система'),
        ('computer_peripherals_included', 'Пристрої введення в комплекті'),
        ('computer_vesa_support', 'Можливість кріплення VESA'),
        ('computer_vr_support', 'З підтримкою VR'),
        ('computer_backlit', 'З підсвічуванням'),
    )
    multi_value_fields = ('computer_wireless_technologies', 'computer_interfaces')
    binary_filter_fields = (
        'computer_optical_drive',
        'computer_card_reader',
        'computer_built_in_microphone',
        'computer_webcam',
        'computer_built_in_speakers',
        'computer_peripherals_included',
        'computer_vesa_support',
        'computer_vr_support',
        'computer_backlit',
    )
    negative_values = {
        'немає',
        'нема',
        'ні',
        'відсутній',
        'відсутня',
        'відсутнє',
        'відсутні',
        'не підтримується',
        'не має',
    }
    positive_values = {
        'є',
        'так',
        'наявний',
        'наявна',
        'наявне',
        'наявні',
        'присутній',
        'присутня',
        'присутнє',
        'присутні',
    }
    value_aliases = {
        'Є': (
            'Є',
            'Так',
            'Наявний',
            'Наявна',
            'Наявне',
            'Наявні',
            'Присутній',
            'Присутня',
            'Присутнє',
            'Присутні',
        ),
        'Немає': (
            'Немає',
            'Нема',
            'Ні',
            'Відсутній',
            'Відсутня',
            'Відсутнє',
            'Відсутні',
            'Не підтримується',
            'Не має',
        ),
    }
    preset_options = {
        'computer_manufacturer': (
            '2E',
            'Acer',
            'Apple',
            'Artline',
            'ASUS',
            'Dell',
            'Expert PC',
            'HP',
            'Lenovo',
            'MSI',
            'Vinga',
        ),
        'computer_type': (
            'Ігрові',
            'Неттопи Vinga',
            'Для роботи та навчання',
            'Робочі станції',
            'Barebone системи',
        ),
        'computer_view': (
            'Класичні',
            'Компактні',
            'Моноблоки',
            'Неттопи',
            'Міні-ПК',
        ),
        'computer_display_diagonal': (
            '10" - 14"',
            '15" - 19"',
            '20" - 23"',
            '23.8"',
            '24" - 26"',
            '27"',
            '28" - 31"',
            '32" і більше',
        ),
        'computer_screen_type': (
            'Звичайний',
            'Сенсорний',
        ),
        'computer_processor_series': (
            'Intel Core 3',
            'Intel Core 5',
            'Intel Core 7',
            'Intel Core 9',
            'Intel Core i3',
            'Intel Core i5',
            'Intel Core i7',
            'Intel Core i9',
            'Intel Core Ultra 5',
            'Intel Core Ultra 7',
            'Intel Core Ultra 9',
            'AMD Ryzen 3',
            'AMD Ryzen 5',
            'AMD Ryzen 7',
            'AMD Ryzen 9',
        ),
        'computer_amd_generation': (
            'Zen',
            'Zen 2',
            'Zen 3',
            'Zen 3+',
            'Zen 4',
            'Zen 5',
        ),
        'computer_intel_generation': (
            '10-е покоління',
            '11-е покоління',
            '12-е покоління',
            '13-е покоління',
            '14-е покоління',
            '15-е покоління',
        ),
        'computer_processor_cores': (
            '2 ядра',
            '4 ядра',
            '6 ядер',
            '8 ядер',
            '10 ядер',
            '12 ядер',
            '14 ядер',
            '16 ядер',
            '20 ядер',
            '24 ядра',
            '32 ядра',
        ),
        'computer_processor_frequency': tuple(option[0] for option in frequency_ranges),
        'computer_graphics_type': (
            'Дискретна',
            'Інтегрована',
            'Вбудована',
        ),
        'computer_discrete_graphics_series': (
            'NVIDIA GeForce RTX 3050',
            'NVIDIA GeForce RTX 3060',
            'NVIDIA GeForce RTX 4060',
            'NVIDIA GeForce RTX 4070',
            'NVIDIA GeForce RTX 4080',
            'NVIDIA GeForce RTX 4090',
            'NVIDIA GeForce RTX 5050',
            'NVIDIA GeForce RTX 5060',
            'NVIDIA GeForce RTX 5070',
            'NVIDIA GeForce RTX 5070 Ti',
            'NVIDIA GeForce RTX 5080',
            'NVIDIA GeForce RTX 5090',
            'AMD Radeon RX 6400',
            'AMD Radeon RX 7600',
            'AMD Radeon RX 7700 XT',
            'AMD Radeon RX 7800 XT',
            'AMD Radeon RX 7900 XT',
            'AMD Radeon RX 9070',
            'AMD Radeon RX 9070 XT',
        ),
        'computer_video_memory': (
            '2 ГБ',
            '4 ГБ',
            '6 ГБ',
            '8 ГБ',
            '10 ГБ',
            '12 ГБ',
            '16 ГБ',
            '24 ГБ',
            '32 ГБ',
        ),
        'computer_ram_capacity': (
            '4 ГБ',
            '8 ГБ',
            '16 ГБ',
            '24 ГБ',
            '32 ГБ',
            '48 ГБ',
            '64 ГБ',
            '96 ГБ',
            '128 ГБ',
            '192 ГБ',
        ),
        'computer_ram_type': ('DDR3', 'DDR4', 'DDR5'),
        'computer_storage_types': ('SSD', 'HDD', 'SSD + HDD', 'Без накопичувача'),
        'computer_hdd_capacity': (
            '500 ГБ',
            '1 ТБ',
            '2 ТБ',
            '4 ТБ',
            'Без HDD',
        ),
        'computer_ssd_capacity': (
            '120 ГБ',
            '240 ГБ',
            '256 ГБ',
            '480 ГБ',
            '500 ГБ',
            '512 ГБ',
            '1 ТБ',
            '2 ТБ',
            '4 ТБ',
            'Без SSD',
        ),
        'computer_optical_drive': ('Є', 'Немає'),
        'computer_card_reader': ('Є', 'Немає'),
        'computer_built_in_microphone': ('Є', 'Немає'),
        'computer_webcam': ('Є', 'Немає'),
        'computer_built_in_speakers': ('Є', 'Немає'),
        'computer_wireless_technologies': (
            'Bluetooth',
            'Wi-Fi',
            'Wi-Fi 5',
            'Wi-Fi 6',
            'Wi-Fi 6E',
            'Wi-Fi 7',
        ),
        'computer_interfaces': (
            'USB',
            'USB 2.0',
            'USB 3.0',
            'USB 3.1',
            'USB 3.2',
            'USB Type-A',
            'USB Type-C',
            'HDMI',
            'DisplayPort',
            'VGA',
            'DVI',
            'LAN (RJ-45)',
            'аудіо',
            'Thunderbolt',
        ),
        'computer_operating_system': (
            'Без ОС',
            'Windows 10 Home',
            'Windows 10 Pro',
            'Windows 11 Home',
            'Windows 11 Pro',
            'Linux',
            'Ubuntu',
            'FreeDOS',
        ),
        'computer_peripherals_included': ('Є', 'Немає'),
        'computer_vesa_support': ('Є', 'Немає'),
        'computer_vr_support': ('Є', 'Немає'),
        'computer_backlit': ('Є', 'Немає'),
    }

    def __init__(self, *args, products, **kwargs):
        super().__init__(*args, products=products, **kwargs)
        if 'computer_processor_frequency' not in self.fields:
            return

        counts = Counter()
        for value in products.values_list('computer_processor_frequency', flat=True):
            frequency = self.parse_frequency(value)
            if frequency is None:
                continue
            for label, minimum, maximum in self.frequency_ranges:
                if (minimum is None or frequency > minimum) and (maximum is None or frequency <= maximum):
                    counts[label] += 1
                    break

        field = self.fields['computer_processor_frequency']
        field.choices = [
            (label, f'{label} ({counts[label]})' if counts[label] else label)
            for label, _, _ in self.frequency_ranges
        ]

    def normalize_filter_value(self, field_name, value):
        value = value.strip()
        normalized = value.casefold()
        if field_name in self.binary_filter_fields:
            if normalized in self.negative_values:
                return 'Немає'
            if field_name == 'computer_optical_drive' and normalized in {
                'без dvd',
                'без dvd-приводу',
                'без оптичного приводу',
            }:
                return 'Немає'
            if normalized in self.positive_values:
                return 'Є'
        return value

    def filter_value_aliases(self, field_name, value):
        if field_name in self.binary_filter_fields:
            normalized = self.normalize_filter_value(field_name, value)
            if normalized in self.value_aliases:
                aliases = list(self.value_aliases[normalized])
                if normalized == 'Немає' and field_name == 'computer_optical_drive':
                    aliases.extend(('Без DVD', 'Без DVD-приводу', 'Без оптичного приводу'))
                return tuple(aliases)
        return (value,)


class ProcessorProductFilterForm(LaptopProductFilterForm):
    filter_fields = (
        ('cpu_manufacturer', 'Виробник'),
        ('cpu_family', 'Сімейство процесора'),
        ('cpu_socket', 'Сокет'),
        ('cpu_core_count', 'Кількість ядер'),
        ('cpu_thread_count', 'Кількість потоків'),
        ('cpu_base_clock', 'Базова тактова частота процесора'),
        ('cpu_max_clock', 'Максимальна тактова частота процесора'),
        ('cpu_tdp', 'Максимальний TDP'),
        ('cpu_integrated_graphics', 'Графічне ядро'),
        ('cpu_intel_generation', 'Покоління процесорів Intel'),
        ('cpu_amd_architecture', 'Архітектура ядра AMD'),
        ('cpu_package_type', 'Тип поставки'),
        ('cpu_cooling_included', 'Охолодження в комплекті'),
    )
    preset_options = {
        'cpu_manufacturer': ('AMD', 'Intel'),
        'cpu_family': (
            'AMD Ryzen Threadripper PRO',
            'Ryzen PRO',
            'AMD Ryzen 3',
            'AMD Ryzen 5',
            'AMD Ryzen 7',
            'AMD Ryzen 9',
            'Intel Core i3',
            'Intel Core i5',
            'Intel Core i7',
            'Intel Core i9',
            'Intel Pentium',
            'Intel Celeron',
            'AMD Ryzen Threadripper',
            'AMD Athlon',
            'Intel Core Ultra 5',
            'Intel Core Ultra 7',
        ),
        'cpu_socket': ('AM4', 'AM5', 'TR5', '1151', '1200', '1700', '1851'),
        'cpu_core_count': ('2 ядра', '4 ядра', '6 ядер', '8 ядер', '10 ядер', '12 ядер'),
        'cpu_thread_count': (
            '2 потоки',
            '4 потоки',
            '8 потоків',
            '12 потоків',
            '16 потоків',
            '20 потоків',
            '24 потоки',
            '28 потоків',
            '32 потоки',
            '48 потоків',
            '10 потоків',
            '14 потоків',
            '18 потоків',
        ),
        'cpu_base_clock': (
            '2.0 GHz',
            '2.1 GHz',
            '2.4 GHz',
            '2.5 GHz',
            '2.6 GHz',
            '3.0 GHz',
            '3.2 GHz',
            '3.3 GHz',
            '3.4 GHz',
            '3.5 GHz',
            '3.6 GHz',
            '3.7 GHz',
            '3.8 GHz',
            '3.9 GHz',
            '4.0 GHz',
            '4.1 GHz',
            '4.2 GHz',
            '4.3 GHz',
            '4.4 GHz',
            '4.5 GHz',
            '4.7 GHz',
        ),
        'cpu_max_clock': (
            '4.0 GHz',
            '4.1 GHz',
            '4.2 GHz',
            '4.3 GHz',
            '4.4 GHz',
            '4.5 GHz',
            '4.6 GHz',
            '4.7 GHz',
            '4.8 GHz',
            '4.9 GHz',
            '5.0 GHz',
            '5.1 GHz',
            '5.2 GHz',
            '5.3 GHz',
            '5.4 GHz',
            '5.5 GHz',
            '5.6 GHz',
            '5.7 GHz',
            '5.8 GHz',
            '6.0 GHz',
        ),
        'cpu_tdp': (
            '35 Вт',
            '46 Вт',
            '54 Вт',
            '58 Вт',
            '60 Вт',
            '65 Вт',
            '95 Вт',
            '105 Вт',
            '110 Вт',
            '120 Вт',
            '121 Вт',
            '125 Вт',
            '148 Вт',
            '154 Вт',
            '159 Вт',
            '170 Вт',
            '200 Вт',
            '219 Вт',
            '250 Вт',
            '253 Вт',
            '350 Вт',
        ),
        'cpu_integrated_graphics': (
            'AMD Radeon 740M',
            'AMD Radeon 760M',
            'AMD Radeon 780M',
            'AMD Radeon Graphics',
            'Intel Graphics',
            'Intel HD 610',
            'Intel UHD 610',
            'Intel UHD 630',
            'Intel UHD 710',
            'Intel UHD 730',
            'Intel UHD 770',
            'Radeon Vega 11',
            'Radeon Vega 3',
            'Radeon Vega 6',
            'Radeon Vega 8',
            'Intel HD Graphics',
            'Немає',
        ),
        'cpu_intel_generation': (
            'Comet Lake (10 покоління)',
            'Kaby Lake (7 покоління)',
            'Rocket Lake (11 покоління)',
            'Alder Lake (12 покоління)',
            'Raptor Lake (13 покоління)',
            'Raptor Lake Refresh (14 покоління)',
            'Arrow Lake (15 покоління)',
        ),
        'cpu_amd_architecture': ('AMD Zen', 'AMD Zen+', 'AMD Zen 2', 'AMD Zen 3', 'AMD Zen 4', 'AMD Zen 5'),
        'cpu_package_type': ('BOX', 'BOX без кулера', 'Tray', 'Tray+кулер'),
        'cpu_cooling_included': ('без кулера', 'кулер у комплекті'),
    }

    def normalize_filter_value(self, field_name, value):
        value = value.strip()
        if field_name == 'cpu_manufacturer':
            return {'amd': 'AMD', 'intel': 'Intel'}.get(value.casefold(), value)
        return value


class MotherboardProductFilterForm(LaptopProductFilterForm):
    available_today = forms.BooleanField(label='Отримати сьогодні', required=False)

    filter_fields = (
        ('motherboard_manufacturer', 'Виробник'),
        ('motherboard_purpose', 'Призначення'),
        ('motherboard_product_socket', 'Сокет'),
        ('motherboard_pcie_x1_slots', 'PCI Express x1'),
        ('motherboard_pcie_x4_slots', 'PCI Express x4'),
        ('motherboard_pcie_x16_slots', 'PCI Express x16'),
        ('motherboard_pci_slots', 'PCI'),
        ('motherboard_chipset_model', 'Модель чипсета'),
        ('motherboard_ram_type', 'Тип оперативної пам’яті'),
        ('motherboard_ram_slots', 'Кількість роз’ємів оперативної пам’яті'),
        ('motherboard_max_ram', 'Максимальний об’єм оперативної пам’яті'),
        ('motherboard_max_ram_frequency', 'Максимальна частота оперативної пам’яті'),
        ('motherboard_integrated_video', 'Вбудоване відео'),
        ('motherboard_lan_speed', 'Швидкість LAN портів'),
        ('motherboard_video_outputs', 'Відеовиходи'),
        ('motherboard_usb', 'USB'),
        ('motherboard_digital_audio_output', 'Цифровий аудіо роз’єм (S/PDIF)'),
        ('motherboard_m2_slots', 'M.2'),
        ('motherboard_sata3_ports', 'Кількість SATA-III портів'),
        ('motherboard_satae_slot', 'SATAe роз’єм'),
        ('motherboard_u2_slot', 'U.2 роз’єм'),
        ('motherboard_wireless', 'Бездротовий зв’язок'),
        ('motherboard_raid_controller', 'Контролер RAID'),
        ('motherboard_search_tag', 'Також шукають'),
        ('motherboard_form_factor', 'Форм-фактор'),
    )
    multi_value_fields = ('motherboard_video_outputs', 'motherboard_usb', 'motherboard_wireless')
    preset_options = {
        'motherboard_manufacturer': ('ASRock', 'ASUS', 'GIGABYTE', 'MSI'),
        'motherboard_purpose': ('геймерська', 'звичайна'),
        'motherboard_product_socket': ('з вбудованим процесором', 'AM4', 'AM5', '1700', '1851'),
        'motherboard_pcie_x1_slots': ('1 шт', '2 шт', '3 шт', '4 шт'),
        'motherboard_pcie_x4_slots': ('1 шт',),
        'motherboard_pcie_x16_slots': ('1 шт', '2 шт', '3 шт', '4 шт', '5 шт', '6 шт'),
        'motherboard_pci_slots': ('без слота PCI', '1 шт', '2 шт'),
        'motherboard_chipset_model': (
            'SOC',
            'AMD B450',
            'AMD A520',
            'AMD B550',
            'Intel H610',
            'AMD A620',
            'AMD B650',
            'Intel B660',
            'Intel B760',
            'Intel Z790',
            'AMD B840',
            'AMD B850',
            'Intel B860',
            'AMD X870',
            'AMD X870E',
            'Intel Z890',
        ),
        'motherboard_ram_type': ('DDR4', 'SO-DIMM DDR4', 'DDR5'),
        'motherboard_ram_slots': ('1 шт', '2 шт', '4 шт'),
        'motherboard_max_ram': ('16 GB', '64 GB', '128 GB', '192 GB', '256 GB'),
        'motherboard_max_ram_frequency': (
            '3200 MHz',
            '4400 MHz',
            '4600 MHz',
            '4733 MHz',
            '4800 MHz',
            '5066 MHz',
            '5333 MHz',
            '5600 MHz',
            '6400 MHz',
            '7200 MHz',
            '7600 MHz',
            '8000 MHz',
            '8400 MHz',
            '8800 MHz',
            '9200 MHz',
            '9600 MHz',
        ),
        'motherboard_integrated_video': (
            'Без підтримки вбудованого відео',
            'З підтримкою відеоядра процесора',
        ),
        'motherboard_lan_speed': ('1 Гбіт/с', '2,5 Гбіт/с', '5 Гбіт/с', '10 Гбіт/с'),
        'motherboard_video_outputs': (
            'D-Sub (VGA)',
            'DisplayPort',
            'DVI',
            'HDMI',
            'Thunderbolt',
            '1 x DisplayPort 1.2',
            '1 x HDMI',
            '1 x VGA',
            '2 x DisplayPort 1.4',
            '2 x USB4 (40Gbps) Type-C',
        ),
        'motherboard_usb': (
            'USB Type-C',
            'USB 2.0',
            'USB 3.0',
            'USB 3.1',
            'USB 3.2',
            'USB4',
            '1 x USB 3.2 Gen1 Type-C',
            '1 x USB 3.2 Gen2 Type-C',
            '2 x USB 2.0',
            '2 x USB 3.2 Gen2 Type-A',
            '2 x USB 3.2 Gen2 Type-C',
            '3 x USB 3.2 Gen1 Type-A',
            '4 x USB 3.2 Gen1 Type-A',
            '5 x USB 2.0',
            '5 x USB 3.2 Gen1 Type-A',
            '9 x USB 3.2 Gen2 Type-A',
        ),
        'motherboard_digital_audio_output': (
            'без цифрового аудіо виходу',
            'коаксіальний + оптичний',
            'оптичний',
            '1 x optical SPDIF out',
        ),
        'motherboard_m2_slots': ('1 шт', '2 шт', '3 шт', '4 шт', '5 шт', 'без M.2 інтерфейсу'),
        'motherboard_sata3_ports': ('1 шт', '2 шт', '4 шт', '6 шт', '7 шт'),
        'motherboard_satae_slot': ('без SATAe інтерфейсу',),
        'motherboard_u2_slot': ('без U.2 роз’єму',),
        'motherboard_wireless': (
            'Bluetooth',
            '802.11 a/b/g/n/ac',
            '802.11 a/b/g/n/ac/ax',
            '802.11 a/b/g/n/ac/ax/be',
        ),
        'motherboard_raid_controller': ('0', '1', '5', '10', 'Без контролера RAID'),
        'motherboard_search_tag': ('материнська плата для ПК',),
        'motherboard_form_factor': ('ATX', 'Mini ITX', 'Micro ATX'),
    }

    def __init__(self, *args, products, **kwargs):
        super().__init__(*args, products=products, **kwargs)
        self.available_today_count = products.filter(motherboard_available_today=True).count()


class VideoCardProductFilterForm(LaptopProductFilterForm):
    filter_fields = (
        ('video_card_manufacturer', 'Виробник'),
        ('video_card_family', 'Сімейство графіки'),
        ('video_card_form_factor', 'Форм-фактор'),
        ('video_card_purpose', 'Призначення'),
        ('video_card_chip', 'Графічний чип'),
        ('video_card_interface', 'Інтерфейс'),
        ('video_card_memory_capacity', 'Об’єм вбудованої пам’яті'),
        ('video_card_memory_type', 'Тип пам’яті'),
        ('video_card_memory_bus', 'Розрядність шини пам’яті'),
        ('video_card_connectors', 'Роз’єми'),
        ('video_card_cooling_system', 'Тип системи охолодження'),
        ('video_card_cooling_type', 'Вид охолодження'),
        ('video_card_fan_count', 'Кількість вентиляторів'),
        ('video_card_power_connectors', 'Роз’єми додаткового живлення'),
    )
    multi_value_fields = ('video_card_connectors',)
    preset_options = {
        'video_card_manufacturer': ('Afox', 'ASUS', 'GIGABYTE', 'HP', 'MSI', 'PNY'),
        'video_card_family': ('NVIDIA', 'AMD'),
        'video_card_form_factor': ('міні', 'низькопрофільна', 'стандартна'),
        'video_card_purpose': ('для майнінгу', 'звичайна', 'професійна', 'ігрова'),
        'video_card_chip': (
            'Quadro RTX 400',
            'Radeon RX 580',
            'Geforce GT 710',
            'GeForce GT 730',
            'Quadro RTX A1000',
            'GeForce GT 1030',
            'RTX PRO 2000',
            'GeForce RTX 3050',
            'GeForce RTX 3060',
            'GeForce RTX 5050',
            'GeForce RTX 5060',
            'GeForce RTX 5060 Ti',
            'GeForce RTX 5070',
            'GeForce RTX 5070 Ti',
            'GeForce RTX 5080',
            'Radeon RX 7600',
            'Radeon RX 9060 XT',
            'Radeon RX 9070 GRE',
            'Radeon RX 9070 XT',
        ),
        'video_card_interface': (
            'PCI-Express 2.0',
            'PCI-Express 3.0',
            'PCI-Express 4.0',
            'PCI-Express 5.0',
        ),
        'video_card_memory_capacity': ('2 ГБ', '4 ГБ', '6 ГБ', '8 ГБ', '12 ГБ', '16 ГБ'),
        'video_card_memory_type': ('DDR3', 'GDDR3', 'DDR4', 'GDDR5', 'GDDR6', 'GDDR7'),
        'video_card_memory_bus': ('64 Bit', '96 Bit', '128 Bit', '192 Bit', '256 Bit'),
        'video_card_connectors': ('DisplayPort', 'DVI', 'HDMI', 'VGA (D-Sub)'),
        'video_card_cooling_system': ('активний', 'пасивний'),
        'video_card_cooling_type': ('кулер', 'радіатор', 'турбіна'),
        'video_card_fan_count': ('1 шт', '2 шт', '3 шт'),
        'video_card_power_connectors': (
            'відсутнє',
            '6 pin',
            '8 + 8 + 8 pin',
            '8 + 8 pin',
            '8 pin',
            '16 pin',
        ),
    }

    def filter_value_aliases(self, field_name, value):
        if field_name == 'video_card_connectors' and value.casefold() == 'vga (d-sub)':
            return (value, 'VGA')
        return (value.strip(),)

    def normalize_filter_value(self, field_name, value):
        value = value.strip()
        if field_name == 'video_card_connectors':
            for connector in self.preset_options[field_name]:
                if connector.casefold() in value.casefold():
                    return connector
            if re.search(r'\bvga\b', value, re.IGNORECASE):
                return 'VGA (D-Sub)'
        return value


class MemoryProductFilterForm(LaptopProductFilterForm):
    filter_fields = (
        ('memory_purpose', 'Призначення'),
        ('memory_manufacturer', 'Виробник'),
        ('memory_type', 'Тип пам’яті'),
        ('memory_capacity', 'Об’єм пам’яті'),
        ('memory_frequency', 'Частота пам’яті'),
        ('memory_module_count', 'Кількість модулів у наборі'),
        ('memory_timing', 'Таймінги'),
        ('memory_voltage', 'Напруга живлення'),
        ('memory_cooling', 'Охолодження'),
        ('memory_lighting', 'Підсвічування'),
        ('memory_overclock_profiles', 'Розширені профілі розгону'),
    )
    multi_value_fields = ('memory_overclock_profiles',)
    preset_options = {
        'memory_purpose': ('для ноутбуків', 'для ПК', 'для серверів'),
        'memory_manufacturer': (
            'AMD',
            'Apacer',
            'Corsair',
            'eXceleram',
            'Fury',
            'G.Skill',
            'Golden Memory',
            'Goodram',
            'Hynix',
            'INTELIGENTES',
            'Kingston',
            'Kingston Fury (ex.HyperX)',
            'Lexar',
            'Micron',
            'Patriot',
            'PNY',
            'Prologix',
            'Samsung',
            'Silicon Power',
            'Synology',
            'Team',
            'Transcend',
            'Wibrand',
        ),
        'memory_type': ('DDR3', 'DDR4', 'DDR5'),
        'memory_capacity': (
            '4 ГБ',
            '8 ГБ',
            '16 ГБ',
            '24 ГБ',
            '32 ГБ',
            '48 ГБ',
            '64 ГБ',
            '96 ГБ',
            '128 ГБ',
        ),
        'memory_frequency': (
            '1333 МГц',
            '1600 МГц',
            '2400 МГц',
            '2666 МГц',
            '3000 МГц',
            '3200 МГц',
            '3600 МГц',
            '4000 МГц',
            '4800 МГц',
            '5200 МГц',
            '5600 МГц',
            '6000 МГц',
            '6400 МГц',
            '6800 МГц',
            '7200 МГц',
            '7600 МГц',
            '8000 МГц',
            '8400 МГц',
            '8800 МГц',
        ),
        'memory_module_count': ('1', '2', '4'),
        'memory_timing': (
            'CL9',
            'CL11',
            'CL16',
            'CL17',
            'CL18',
            'CL19',
            'CL20',
            'CL22',
            'CL28',
            'CL30',
            'CL32',
            'CL34',
            'CL36',
            'CL38',
            'CL40',
            'CL42',
            'CL46',
            'CL48',
            'CL52',
            'CL58',
        ),
        'memory_voltage': ('1.1 В', '1.2 В', '1.25 В', '1.35 В', '1.4 В', '1.45 В', '1.5 В'),
        'memory_cooling': ('радіатор', 'немає'),
        'memory_lighting': ('немає', 'є'),
        'memory_overclock_profiles': ('EXPO', 'XMP'),
    }
