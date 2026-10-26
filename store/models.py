from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField('Назва', max_length=200)
    category = models.CharField('Категорія', max_length=100)
    price = models.DecimalField(
        'Ціна',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    image_url = models.URLField('Посилання на фото', blank=True)
    badge = models.CharField('Бейдж', max_length=50, blank=True)
    is_active = models.BooleanField('Опублікований', default=True)
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'товар'
        verbose_name_plural = 'товари'

    def __str__(self):
        return self.name
