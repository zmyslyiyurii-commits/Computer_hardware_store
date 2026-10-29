from django.core.validators import MinValueValidator
from django.db import models


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
    image_url = models.URLField('Посилання на фото', blank=True)
    badge = models.CharField('Бейдж', max_length=50, blank=True)
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
