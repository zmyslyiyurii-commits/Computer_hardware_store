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
    # Неопубліковані товари залишаються в адмінці, але не показуються покупцям.
    is_active = models.BooleanField('Опублікований', default=True)
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'товар'
        verbose_name_plural = 'товари'

    def __str__(self):
        return self.name
