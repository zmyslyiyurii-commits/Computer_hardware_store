import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0008_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Кількість на складі'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=150, verbose_name='Ім’я та прізвище')),
                ('phone', models.CharField(max_length=30, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Електронна пошта')),
                ('delivery_address', models.CharField(max_length=255, verbose_name='Адреса доставки')),
                ('total', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сума замовлення')),
                ('status', models.CharField(choices=[('new', 'Нове'), ('processing', 'В обробці'), ('completed', 'Виконане'), ('cancelled', 'Скасоване')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
            ],
            options={
                'verbose_name': 'замовлення',
                'verbose_name_plural': 'замовлення',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100, verbose_name='Ім’я')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Оцінка')),
                ('text', models.TextField(verbose_name='Відгук')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Опублікований')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Додано')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'відгук',
                'verbose_name_plural': 'відгуки',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(condition=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='review_rating_between_1_and_5'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, verbose_name='Назва товару')),
                ('quantity', models.PositiveIntegerField(verbose_name='Кількість')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна за одиницю')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order', verbose_name='Замовлення')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'позиція замовлення',
                'verbose_name_plural': 'позиції замовлення',
            },
        ),
    ]
