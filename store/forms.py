from collections import Counter

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
                        value.strip()
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
                counts = {option[field_name]: option['product_count'] for option in options}
            values = list(self.preset_options[field_name])
            values.extend(sorted(
                (value for value in counts if value not in values),
                key=str.casefold,
            ))
            choices = [
                (
                    value,
                    f'{value} ({counts[value]})' if counts.get(value, 0) else value,
                )
                for value in values
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

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')

        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValidationError('Мінімальна ціна не може бути більшою за максимальну.')

        return cleaned_data
