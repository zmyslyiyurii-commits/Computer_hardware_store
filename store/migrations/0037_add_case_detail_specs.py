from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0036_add_case_filter_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='case_external_bays_5_25',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість зовнішніх відсіків 5.25"'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_external_bays_3_5',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість зовнішніх відсіків 3.5"'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_internal_bays_5_25',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість внутрішніх відсіків 5.25"'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_internal_bays_2_5',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість внутрішніх відсіків 2.5"'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_expansion_slots',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість слотів розширення'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_additional_fan_positions',
            field=models.TextField(blank=True, verbose_name='Місця для додаткових вентиляторів'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_cooling_elements',
            field=models.TextField(blank=True, verbose_name='Охолоджуючі елементи корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_dust_filter',
            field=models.CharField(blank=True, max_length=30, verbose_name='Пиловий фільтр корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_liquid_cooling_support',
            field=models.CharField(blank=True, max_length=30, verbose_name='Підтримка рідинного охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_max_noise',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальний рівень шуму корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_gpu_clearance',
            field=models.CharField(blank=True, max_length=30, verbose_name='Встановлення довгих відеокарт'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_cpu_cooler_clearance',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальна висота процесорного кулера'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_dimensions',
            field=models.CharField(blank=True, max_length=60, verbose_name='Розмір корпусу, мм'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_weight',
            field=models.CharField(blank=True, max_length=30, verbose_name='Вага корпусу, кг'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод корпусу'),
        ),
    ]
