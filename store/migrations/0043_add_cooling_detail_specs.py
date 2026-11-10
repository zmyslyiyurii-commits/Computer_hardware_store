from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0042_add_cooling_catalog_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cooling_max_fan_speed',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальна частота обертів вентиляторів системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_radiator_material',
            field=models.CharField(blank=True, max_length=60, verbose_name='Матеріал радіатора системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_airflow',
            field=models.CharField(blank=True, max_length=30, verbose_name='Повітряний потік системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_fan_speed_control',
            field=models.CharField(blank=True, max_length=30, verbose_name='Управління швидкістю обертання вентиляторів'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_pump_power_connector',
            field=models.CharField(blank=True, max_length=40, verbose_name='Роз’єм живлення помпи'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_fan_power_connector',
            field=models.CharField(blank=True, max_length=40, verbose_name='Роз’єм живлення вентиляторів'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_pump_voltage',
            field=models.CharField(blank=True, max_length=20, verbose_name='Напруга живлення помпи'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_tube_length',
            field=models.CharField(blank=True, max_length=30, verbose_name='Довжина патрубків системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_radiator_dimensions',
            field=models.CharField(blank=True, max_length=60, verbose_name='Розміри радіатора системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_fan_dimensions',
            field=models.CharField(blank=True, max_length=60, verbose_name='Розміри вентиляторів системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_pump_dimensions',
            field=models.CharField(blank=True, max_length=60, verbose_name='Розмір водоблоку системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія системи охолодження, міс.'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='cooling_note',
            field=models.TextField(blank=True, verbose_name='Примітка до системи охолодження'),
        ),
    ]
