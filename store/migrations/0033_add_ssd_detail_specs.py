from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0032_product_ssd_filter_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ssd_endurance',
            field=models.CharField(blank=True, max_length=40, verbose_name='Напрацювання на відмову SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_tbw',
            field=models.CharField(blank=True, max_length=30, verbose_name='TBW SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_power_consumption',
            field=models.CharField(blank=True, max_length=30, verbose_name='Енергоспоживання SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_dimensions',
            field=models.CharField(blank=True, max_length=100, verbose_name='Габарити SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_weight',
            field=models.CharField(blank=True, max_length=30, verbose_name='Вага SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_color',
            field=models.CharField(blank=True, max_length=30, verbose_name='Колір SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія SSD, міс.'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_note',
            field=models.TextField(blank=True, verbose_name='Примітка до SSD'),
        ),
    ]
