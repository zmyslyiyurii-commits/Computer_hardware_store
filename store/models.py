from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import F


class Category(models.Model):
    # Категорія об'єднує товари одного типу, наприклад ноутбуки чи монітори.
    name = models.CharField('Назва', max_length=100, unique=True)
    icon = models.CharField('Іконка', max_length=8, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категорія'
        verbose_name_plural = 'категорії'

    def __str__(self):
        return self.name


class Product(models.Model):
    # Основні дані товару, які редагуються через адміністративну панель.
    name = models.CharField('Назва', max_length=200)
    category = models.ForeignKey(
        Category,
        # Не дозволяємо видалити категорію, поки до неї прив'язані товари.
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категорія',
    )
    price = models.DecimalField(
        'Ціна',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    stock_quantity = models.PositiveIntegerField('Кількість на складі', default=0)
    image_url = models.URLField('Посилання на фото', blank=True)
    badge = models.CharField('Бейдж', max_length=50, blank=True)
    description = models.TextField('Опис', blank=True)
    manufacturer = models.CharField('Виробник', max_length=100, blank=True)
    model_series = models.CharField('Серія (модельний ряд)', max_length=100, blank=True)
    laptop_type = models.CharField('Тип ноутбуку', max_length=60, blank=True)
    display_diagonal = models.CharField('Діагональ дисплея', max_length=30, blank=True)
    resolution = models.CharField('Роздільна здатність', max_length=30, blank=True)
    matrix_type = models.CharField('Тип матриці', max_length=30, blank=True)
    screen_surface = models.CharField('Поверхня екрану', max_length=40, blank=True)
    refresh_rate = models.CharField('Частота оновлення екрану', max_length=20, blank=True)
    intel_generation = models.CharField('Покоління процесора Intel', max_length=30, blank=True)
    amd_generation = models.CharField('Покоління процесора AMD', max_length=30, blank=True)
    processor = models.CharField('Процесор', max_length=100, blank=True)
    processor_cores = models.CharField('Кількість ядер процесора', max_length=10, blank=True)
    ram_type = models.CharField("Тип оперативної пам'яті", max_length=20, blank=True)
    ram_capacity = models.CharField("Об'єм оперативної пам'яті", max_length=20, blank=True)
    ram_slots = models.CharField('Кількість слотів для оперативної пам’яті', max_length=50, blank=True)
    ssd_capacity = models.CharField('Об’єм SSD', max_length=30, blank=True)
    graphics_type = models.CharField('Тип відеокарти', max_length=30, blank=True)
    discrete_graphics_series = models.CharField('Серія дискретної відеокарти', max_length=100, blank=True)
    video_memory = models.CharField('Об’єм відеопам’яті', max_length=30, blank=True)
    wireless_technologies = models.TextField(
        'Бездротові технології',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    interfaces = models.TextField(
        'Інтерфейси та підключення',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    operating_system = models.CharField('Операційна система', max_length=100, blank=True)
    battery_capacity = models.CharField('Ємність акумулятора', max_length=40, blank=True)
    webcam = models.CharField('Веб-камера', max_length=100, blank=True)
    additional_features = models.TextField('Додаткові можливості', blank=True)
    width = models.CharField('Ширина, мм', max_length=30, blank=True)
    height = models.CharField('Висота, мм', max_length=30, blank=True)
    depth = models.CharField('Глибина, мм', max_length=30, blank=True)
    country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    features = models.TextField(
        'Особливості',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    weight = models.CharField('Вага', max_length=30, blank=True)
    color = models.CharField('Колір', max_length=30, blank=True)
    computer_type = models.CharField('Тип ПК', max_length=60, blank=True)
    computer_view = models.CharField('Вид комп’ютера', max_length=60, blank=True)
    processor_threads = models.CharField('Кількість потоків', max_length=20, blank=True)
    processor_frequency = models.CharField('Частота процесора, ГГц', max_length=30, blank=True)
    processor_boost_frequency = models.CharField('Частота в Boost, ГГц', max_length=30, blank=True)
    processor_boost_supported = models.CharField('Підтримка Boost режиму', max_length=30, blank=True)
    motherboard_socket = models.CharField('Сокет', max_length=40, blank=True)
    motherboard_chipset = models.CharField('Чипсет', max_length=100, blank=True)
    graphics_card_manufacturer = models.CharField('Виробник чипу відеокарти', max_length=100, blank=True)
    ram_form_factor = models.CharField('Форм-фактор пам’яті', max_length=40, blank=True)
    ram_frequency = models.CharField('Частота пам’яті', max_length=40, blank=True)
    ram_standard = models.CharField('Стандарт пам’яті', max_length=40, blank=True)
    ram_max_capacity = models.CharField('Максимальний об’єм пам’яті', max_length=40, blank=True)
    storage_types = models.CharField('Типи внутрішніх накопичувачів', max_length=100, blank=True)
    hdd_capacity = models.CharField('Об’єм HDD', max_length=40, blank=True)
    optical_drive = models.CharField('Оптичний привід', max_length=60, blank=True)
    card_reader = models.CharField('Кардридер', max_length=60, blank=True)
    built_in_microphone = models.CharField('Вбудований мікрофон', max_length=60, blank=True)
    built_in_speakers = models.CharField('Вбудовані динаміки', max_length=60, blank=True)
    audio_controller = models.CharField('Аудіоконтролер', max_length=150, blank=True)
    multichannel_audio = models.CharField('Багатоканальний звук', max_length=40, blank=True)
    wired_network = models.CharField('Провідна мережа (LAN)', max_length=80, blank=True)
    peripherals_included = models.CharField('Пристрої введення в комплекті', max_length=150, blank=True)
    case_model = models.CharField('Модель корпусу', max_length=100, blank=True)
    case_metal_thickness = models.CharField('Товщина металу корпусу', max_length=40, blank=True)
    case_material = models.CharField('Матеріал корпусу', max_length=100, blank=True)
    psu_location = models.CharField('Розташування блоку живлення', max_length=60, blank=True)
    psu_power = models.CharField('Потужність блоку живлення', max_length=40, blank=True)
    case_lighting = models.CharField('Підсвічування корпусу', max_length=150, blank=True)
    cooling = models.TextField('Охолодження', blank=True)
    computer_manufacturer = models.CharField('Виробник', max_length=100, blank=True)
    computer_display_diagonal = models.CharField('Діагональ екрану', max_length=30, blank=True)
    computer_screen_type = models.CharField('Тип екрану', max_length=50, blank=True)
    computer_processor_series = models.CharField('Серія процесора', max_length=100, blank=True)
    computer_intel_generation = models.CharField('Покоління процесора Intel', max_length=30, blank=True)
    computer_amd_generation = models.CharField('Покоління процесора AMD', max_length=30, blank=True)
    computer_processor = models.CharField('Модель процесора', max_length=100, blank=True)
    computer_processor_cores = models.CharField('Кількість ядер процесора', max_length=10, blank=True)
    computer_ram_type = models.CharField("Тип оперативної пам'яті", max_length=20, blank=True)
    computer_ram_capacity = models.CharField("Об'єм оперативної пам'яті", max_length=20, blank=True)
    computer_ram_slots = models.CharField('Кількість слотів пам’яті', max_length=50, blank=True)
    computer_ram_frequency = models.CharField('Частота пам’яті', max_length=40, blank=True)
    computer_ram_standard = models.CharField('Стандарт пам’яті', max_length=40, blank=True)
    computer_ram_max_capacity = models.CharField('Максимальний об’єм пам’яті', max_length=40, blank=True)
    computer_ssd_capacity = models.CharField('Об’єм SSD', max_length=30, blank=True)
    computer_graphics_type = models.CharField('Тип відеокарти', max_length=30, blank=True)
    computer_discrete_graphics_series = models.CharField('Модель відеокарти', max_length=100, blank=True)
    computer_video_memory = models.CharField('Об’єм відеопам’яті', max_length=30, blank=True)
    computer_wireless_technologies = models.TextField(
        'Бездротові технології',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    computer_interfaces = models.TextField(
        'Зовнішні порти та роз’єми',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    computer_operating_system = models.CharField('Операційна система', max_length=100, blank=True)
    computer_webcam = models.CharField('Вбудована веб-камера', max_length=100, blank=True)
    computer_additional_features = models.TextField('Додаткові можливості', blank=True)
    computer_vesa_support = models.CharField('Можливість кріплення VESA', max_length=40, blank=True)
    computer_vr_support = models.CharField('Підтримка VR', max_length=40, blank=True)
    computer_backlit = models.CharField('Підсвічування', max_length=40, blank=True)
    computer_width = models.CharField('Ширина корпусу, мм', max_length=30, blank=True)
    computer_height = models.CharField('Висота корпусу, мм', max_length=30, blank=True)
    computer_depth = models.CharField('Глибина корпусу, мм', max_length=30, blank=True)
    computer_country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    computer_warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    computer_features = models.TextField('Примітка', blank=True)
    computer_weight = models.CharField('Вага', max_length=30, blank=True)
    computer_color = models.CharField('Колір корпусу', max_length=30, blank=True)
    computer_processor_frequency = models.CharField('Частота процесора, ГГц', max_length=30, blank=True)
    computer_storage_types = models.CharField('Типи внутрішніх накопичувачів', max_length=100, blank=True)
    computer_hdd_capacity = models.CharField('Об’єм HDD', max_length=40, blank=True)
    computer_optical_drive = models.CharField('Оптичний привід', max_length=60, blank=True)
    computer_card_reader = models.CharField('Кардридер', max_length=60, blank=True)
    computer_built_in_microphone = models.CharField('Вбудований мікрофон', max_length=60, blank=True)
    computer_built_in_speakers = models.CharField('Вбудовані динаміки', max_length=60, blank=True)
    computer_audio_controller = models.CharField('Аудіоконтролер', max_length=150, blank=True)
    computer_multichannel_audio = models.CharField('Багатоканальний звук', max_length=40, blank=True)
    computer_wired_network = models.CharField('Провідна мережа (LAN)', max_length=80, blank=True)
    computer_peripherals_included = models.CharField('Пристрої введення в комплекті', max_length=150, blank=True)
    # Неопубліковані товари залишаються в адмінці, але не показуються покупцям.
    is_active = models.BooleanField('Опублікований', default=True)
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'товар'
        verbose_name_plural = 'товари'

    def __str__(self):
        return self.name

    @property
    def product_code(self):
        return f'NXS-{self.pk:06d}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Товар',
    )
    image_url = models.URLField(
        'URL додаткового фото',
        max_length=1000,
        help_text='Встав повне посилання на зображення, наприклад https://example.com/photo.jpg.',
    )
    alt_text = models.CharField('Опис фото', max_length=200, blank=True)
    position = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ('position', 'pk')
        verbose_name = 'фото товару'
        verbose_name_plural = 'фотографії товару'

    def __str__(self):
        return self.alt_text or f'Фото: {self.product.name}'


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name='Користувач',
    )
    phone = models.CharField('Телефон', max_length=30, blank=True)

    class Meta:
        verbose_name = 'профіль покупця'
        verbose_name_plural = 'профілі покупців'

    def __str__(self):
        return f'Профіль: {self.user.username}'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар',
    )
    author_name = models.CharField('Ім’я', max_length=100)
    rating = models.PositiveSmallIntegerField('Оцінка')
    text = models.TextField('Відгук')
    is_approved = models.BooleanField('Опублікований', default=False)
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'відгук'
        verbose_name_plural = 'відгуки'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name='review_rating_between_1_and_5',
            ),
        ]

    def __str__(self):
        return f'{self.author_name} — {self.product.name} ({self.rating}/5)'


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Нове'),
        ('processing', 'В обробці'),
        ('completed', 'Виконане'),
        ('cancelled', 'Скасоване'),
    )

    customer_name = models.CharField('Ім’я та прізвище', max_length=150)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='store_orders',
        null=True,
        blank=True,
        verbose_name='Акаунт покупця',
    )
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Електронна пошта')
    delivery_address = models.CharField('Адреса доставки', max_length=255)
    total = models.DecimalField('Сума замовлення', max_digits=12, decimal_places=2)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'

    def __str__(self):
        return f'Замовлення №{self.pk}'

    def cancel(self):
        if not self.pk:
            return False

        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=self.pk)
            if order.status not in ('new', 'processing'):
                self.status = order.status
                return False

            for item in order.items.all():
                Product.objects.filter(pk=item.product_id).update(
                    stock_quantity=F('stock_quantity') + item.quantity,
                )

            order.status = 'cancelled'
            order.save(update_fields=('status',))
            self.status = order.status
            return True


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Замовлення',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Товар',
    )
    product_name = models.CharField('Назва товару', max_length=200)
    quantity = models.PositiveIntegerField('Кількість')
    unit_price = models.DecimalField('Ціна за одиницю', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'позиція замовлення'
        verbose_name_plural = 'позиції замовлення'

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'
