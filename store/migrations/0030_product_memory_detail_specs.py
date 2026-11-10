from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0029_product_memory_specs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='memory_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_standard',
            field=models.CharField(blank=True, max_length=40, verbose_name='Стандарти пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_form_factor',
            field=models.CharField(blank=True, max_length=40, verbose_name='Форм-фактор пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_ecc',
            field=models.CharField(blank=True, max_length=20, verbose_name='Перевірка і корекція помилок (ECC)'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_buffering',
            field=models.CharField(blank=True, max_length=30, verbose_name='Буферизація'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_additional_note',
            field=models.TextField(blank=True, verbose_name='Додаткова примітка'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія, міс.'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод'),
        ),
        migrations.AddField(
            model_name='product',
            name='memory_note',
            field=models.TextField(blank=True, verbose_name='Примітка'),
        ),
    ]
