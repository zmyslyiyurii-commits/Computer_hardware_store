from django.core.validators import MinValueValidator
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
    features = models.TextField(
        'Особливості',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    weight = models.CharField('Вага', max_length=30, blank=True)
    color = models.CharField('Колір', max_length=30, blank=True)
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
