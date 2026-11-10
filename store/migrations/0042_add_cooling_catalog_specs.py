from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0041_add_power_supply_origin_and_warranty'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cooling_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_cpu_compatibility',
            field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='Сумісність із процесорами'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_socket',
            field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='Сокет'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_fan_count',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість вентиляторів системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_fan_diameter',
            field=models.CharField(blank=True, max_length=40, verbose_name='Діаметр вентиляторів системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_lighting',
            field=models.CharField(blank=True, max_length=30, verbose_name='Підсвічування системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_max_tdp',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальний TDP системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_noise_level',
            field=models.CharField(blank=True, max_length=30, verbose_name='Рівень шуму системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_color',
            field=models.CharField(blank=True, max_length=40, verbose_name='Колір системи охолодження'),
        ),
    ]
