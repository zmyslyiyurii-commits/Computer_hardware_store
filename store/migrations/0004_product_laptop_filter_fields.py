from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0003_rename_laptop_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник'),
        ),
        migrations.AddField(
            model_name='product',
            name='laptop_type',
            field=models.CharField(blank=True, max_length=60, verbose_name='Тип ноутбуку'),
        ),
        migrations.AddField(
            model_name='product',
            name='display_diagonal',
            field=models.CharField(blank=True, max_length=30, verbose_name='Діагональ дисплея'),
        ),
        migrations.AddField(
            model_name='product',
            name='resolution',
            field=models.CharField(blank=True, max_length=30, verbose_name='Роздільна здатність'),
        ),
        migrations.AddField(
            model_name='product',
            name='matrix_type',
            field=models.CharField(blank=True, max_length=30, verbose_name='Тип матриці'),
        ),
        migrations.AddField(
            model_name='product',
            name='screen_surface',
            field=models.CharField(blank=True, max_length=40, verbose_name='Поверхня екрану'),
        ),
        migrations.AddField(
            model_name='product',
            name='refresh_rate',
            field=models.CharField(blank=True, max_length=20, verbose_name='Частота оновлення екрану'),
        ),
    ]
