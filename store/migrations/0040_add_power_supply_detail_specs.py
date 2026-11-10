from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0039_add_power_supply_filter_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='psu_motherboard_connector',
            field=models.CharField(blank=True, max_length=60, verbose_name='Підключення материнської плати'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_cpu_connector',
            field=models.CharField(blank=True, max_length=60, verbose_name='Підключення процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_gpu_connector',
            field=models.CharField(blank=True, max_length=80, verbose_name='Підключення відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_peripheral_connectors',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість роз’ємів Peripheral'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_output_current_5v',
            field=models.CharField(blank=True, max_length=20, verbose_name='Output Current +5V'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_output_current_3_3v',
            field=models.CharField(blank=True, max_length=20, verbose_name='Output Current +3.3V'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_output_current_12v',
            field=models.CharField(blank=True, max_length=20, verbose_name='Output Current +12V'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_output_current_minus_12v',
            field=models.CharField(blank=True, max_length=20, verbose_name='Output Current -12V'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_output_current_5vsb',
            field=models.CharField(blank=True, max_length=20, verbose_name='Output Current +5Vsb'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_cooling_type',
            field=models.CharField(blank=True, max_length=40, verbose_name='Тип охолодження блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_protection',
            field=models.TextField(blank=True, verbose_name='Захист блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_dimensions',
            field=models.CharField(blank=True, max_length=80, verbose_name='Розмір блоку живлення, мм'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод блоку живлення'),
        ),
    ]
