from django.db import migrations, models


def copy_existing_computer_filter_specs(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    computer_products = Product.objects.using(database).filter(
        category__name__iexact='Комп’ютери',
    )
    for product in computer_products.iterator():
        Product.objects.using(database).filter(pk=product.pk).update(
            computer_ram_frequency=product.ram_frequency,
            computer_ram_standard=product.ram_standard,
            computer_ram_max_capacity=product.ram_max_capacity,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0014_separate_computer_product_specs'),
    ]

    operations = [
        migrations.AddField('product', 'computer_display_diagonal', models.CharField(blank=True, max_length=30, verbose_name='Діагональ екрану')),
        migrations.AddField('product', 'computer_screen_type', models.CharField(blank=True, max_length=50, verbose_name='Тип екрану')),
        migrations.AddField('product', 'computer_processor_series', models.CharField(blank=True, max_length=100, verbose_name='Серія процесора')),
        migrations.AddField('product', 'computer_ram_frequency', models.CharField(blank=True, max_length=40, verbose_name='Частота пам’яті')),
        migrations.AddField('product', 'computer_ram_standard', models.CharField(blank=True, max_length=40, verbose_name='Стандарт пам’яті')),
        migrations.AddField('product', 'computer_ram_max_capacity', models.CharField(blank=True, max_length=40, verbose_name='Максимальний об’єм пам’яті')),
        migrations.AddField('product', 'computer_vesa_support', models.CharField(blank=True, max_length=40, verbose_name='Можливість кріплення VESA')),
        migrations.AddField('product', 'computer_vr_support', models.CharField(blank=True, max_length=40, verbose_name='Підтримка VR')),
        migrations.AddField('product', 'computer_backlit', models.CharField(blank=True, max_length=40, verbose_name='Підсвічування')),
        migrations.RunPython(copy_existing_computer_filter_specs, migrations.RunPython.noop),
    ]
