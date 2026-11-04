from django.db import migrations, models


COMPUTER_FIELD_MAPPINGS = {
    'computer_manufacturer': 'manufacturer',
    'computer_intel_generation': 'intel_generation',
    'computer_amd_generation': 'amd_generation',
    'computer_processor': 'processor',
    'computer_processor_cores': 'processor_cores',
    'computer_ram_type': 'ram_type',
    'computer_ram_capacity': 'ram_capacity',
    'computer_ram_slots': 'ram_slots',
    'computer_ssd_capacity': 'ssd_capacity',
    'computer_graphics_type': 'graphics_type',
    'computer_discrete_graphics_series': 'discrete_graphics_series',
    'computer_video_memory': 'video_memory',
    'computer_wireless_technologies': 'wireless_technologies',
    'computer_interfaces': 'interfaces',
    'computer_operating_system': 'operating_system',
    'computer_webcam': 'webcam',
    'computer_additional_features': 'additional_features',
    'computer_width': 'width',
    'computer_height': 'height',
    'computer_depth': 'depth',
    'computer_country_of_origin': 'country_of_origin',
    'computer_warranty_months': 'warranty_months',
    'computer_features': 'features',
    'computer_weight': 'weight',
    'computer_color': 'color',
}


def copy_existing_computer_specs(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    computer_products = Product.objects.using(database).filter(
        category__name__iexact='Комп’ютери',
    )
    for product in computer_products.iterator():
        updates = {
            computer_field: getattr(product, source_field)
            for computer_field, source_field in COMPUTER_FIELD_MAPPINGS.items()
        }
        Product.objects.using(database).filter(pk=product.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0013_computer_product_specs'),
    ]

    operations = [
        migrations.AddField('product', 'computer_manufacturer', models.CharField(blank=True, max_length=100, verbose_name='Виробник')),
        migrations.AddField('product', 'computer_intel_generation', models.CharField(blank=True, max_length=30, verbose_name='Покоління процесора Intel')),
        migrations.AddField('product', 'computer_amd_generation', models.CharField(blank=True, max_length=30, verbose_name='Покоління процесора AMD')),
        migrations.AddField('product', 'computer_processor', models.CharField(blank=True, max_length=100, verbose_name='Модель процесора')),
        migrations.AddField('product', 'computer_processor_cores', models.CharField(blank=True, max_length=10, verbose_name='Кількість ядер процесора')),
        migrations.AddField('product', 'computer_ram_type', models.CharField(blank=True, max_length=20, verbose_name="Тип оперативної пам'яті")),
        migrations.AddField('product', 'computer_ram_capacity', models.CharField(blank=True, max_length=20, verbose_name="Об'єм оперативної пам'яті")),
        migrations.AddField('product', 'computer_ram_slots', models.CharField(blank=True, max_length=50, verbose_name='Кількість слотів пам’яті')),
        migrations.AddField('product', 'computer_ssd_capacity', models.CharField(blank=True, max_length=30, verbose_name='Об’єм SSD')),
        migrations.AddField('product', 'computer_graphics_type', models.CharField(blank=True, max_length=30, verbose_name='Тип відеокарти')),
        migrations.AddField('product', 'computer_discrete_graphics_series', models.CharField(blank=True, max_length=100, verbose_name='Модель відеокарти')),
        migrations.AddField('product', 'computer_video_memory', models.CharField(blank=True, max_length=30, verbose_name='Об’єм відеопам’яті')),
        migrations.AddField('product', 'computer_wireless_technologies', models.TextField(blank=True, verbose_name='Бездротові технології')),
        migrations.AddField('product', 'computer_interfaces', models.TextField(blank=True, verbose_name='Зовнішні порти та роз’єми')),
        migrations.AddField('product', 'computer_operating_system', models.CharField(blank=True, max_length=100, verbose_name='Операційна система')),
        migrations.AddField('product', 'computer_webcam', models.CharField(blank=True, max_length=100, verbose_name='Вбудована веб-камера')),
        migrations.AddField('product', 'computer_additional_features', models.TextField(blank=True, verbose_name='Додаткові можливості')),
        migrations.AddField('product', 'computer_width', models.CharField(blank=True, max_length=30, verbose_name='Ширина корпусу, мм')),
        migrations.AddField('product', 'computer_height', models.CharField(blank=True, max_length=30, verbose_name='Висота корпусу, мм')),
        migrations.AddField('product', 'computer_depth', models.CharField(blank=True, max_length=30, verbose_name='Глибина корпусу, мм')),
        migrations.AddField('product', 'computer_country_of_origin', models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва')),
        migrations.AddField('product', 'computer_warranty_months', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія, міс.')),
        migrations.AddField('product', 'computer_features', models.TextField(blank=True, verbose_name='Примітка')),
        migrations.AddField('product', 'computer_weight', models.CharField(blank=True, max_length=30, verbose_name='Вага')),
        migrations.AddField('product', 'computer_color', models.CharField(blank=True, max_length=30, verbose_name='Колір корпусу')),
        migrations.RunPython(copy_existing_computer_specs, migrations.RunPython.noop),
    ]
