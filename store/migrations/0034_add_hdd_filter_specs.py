from django.db import migrations, models


def copy_existing_hdd_specs(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for product in Product.objects.filter(component_type='hdd').iterator():
        updates = {}
        if not product.hdd_manufacturer and product.manufacturer:
            updates['hdd_manufacturer'] = product.manufacturer
        if not product.hdd_component_capacity and product.hdd_capacity:
            updates['hdd_component_capacity'] = product.hdd_capacity
        if updates:
            Product.objects.filter(pk=product.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0033_add_ssd_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hdd_drive_type',
            field=models.CharField(blank=True, max_length=40, verbose_name='Тип HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_component_capacity',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм HDD накопичувача'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_form_factor',
            field=models.CharField(blank=True, max_length=20, verbose_name='Форм-фактор HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_rpm',
            field=models.CharField(blank=True, max_length=30, verbose_name='Швидкість обертання HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_buffer_size',
            field=models.CharField(blank=True, max_length=30, verbose_name='Розмір буфера HDD'),
        ),
        migrations.AddField(
            model_name='product',
            name='hdd_interface',
            field=models.CharField(blank=True, max_length=40, verbose_name='Інтерфейс HDD'),
        ),
        migrations.RunPython(copy_existing_hdd_specs, migrations.RunPython.noop),
    ]
