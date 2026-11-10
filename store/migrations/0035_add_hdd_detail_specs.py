from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0034_add_hdd_filter_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hdd_series',
            field=models.CharField(blank=True, max_length=100, verbose_name='Лінійка (серія) HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія HDD, міс.'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_note',
            field=models.TextField(blank=True, verbose_name='Примітка до HDD'),
        ),
    ]
