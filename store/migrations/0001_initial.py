from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва')),
                ('category', models.CharField(max_length=100, verbose_name='Категорія')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)], verbose_name='Ціна')),
                ('image_url', models.URLField(blank=True, verbose_name='Посилання на фото')),
                ('badge', models.CharField(blank=True, max_length=50, verbose_name='Бейдж')),
                ('is_active', models.BooleanField(default=True, verbose_name='Опублікований')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Додано')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товари',
                'ordering': ('-created_at',),
            },
        ),
    ]
