from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0028_product_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='memory_purpose',
            field=models.CharField(blank=True, max_length=40, verbose_name='Призначення оперативної пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник оперативної пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_type',
            field=models.CharField(blank=True, max_length=20, verbose_name='Тип пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_capacity',
            field=models.CharField(blank=True, max_length=20, verbose_name='Об’єм пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_frequency',
            field=models.CharField(blank=True, max_length=20, verbose_name='Частота пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_module_count',
            field=models.CharField(blank=True, max_length=20, verbose_name='Кількість модулів у наборі'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_timing',
            field=models.CharField(blank=True, max_length=20, verbose_name='Таймінги'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_voltage',
            field=models.CharField(blank=True, max_length=20, verbose_name='Напруга живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_cooling',
            field=models.CharField(blank=True, max_length=30, verbose_name='Охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_lighting',
            field=models.CharField(blank=True, max_length=20, verbose_name='Підсвічування'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_overclock_profiles',
            field=models.CharField(
                blank=True,
                help_text='Якщо профілів кілька, розділяйте їх комами.',
                max_length=50,
                verbose_name='Розширені профілі розгону',
            ),
        ),
    ]
