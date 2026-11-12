from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0050_add_network_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thermal_compatibility',
            field=models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Сумісність термопасти',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal_conductivity',
            field=models.CharField(blank=True, max_length=40, verbose_name='Теплопровідність термопасти'),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal_weight',
            field=models.CharField(blank=True, max_length=30, verbose_name='Вага термопасти'),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal_packaging',
            field=models.CharField(blank=True, max_length=40, verbose_name='Тип упаковки термопасти'),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник термопасти'),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва термопасти'),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод термопасти'),
        ),
        migrations.AddField(
            model_name='product',
            name='thermal_note',
            field=models.TextField(blank=True, verbose_name='Примітка до термопасти'),
        ),
    ]
