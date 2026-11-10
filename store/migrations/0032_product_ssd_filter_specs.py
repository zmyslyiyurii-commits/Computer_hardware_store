from django.db import migrations, models


def copy_existing_ssd_capacity(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    Product.objects.filter(
        component_type='ssd',
        ssd_component_capacity='',
    ).exclude(
        ssd_capacity='',
    ).update(ssd_component_capacity=models.F('ssd_capacity'))


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0031_split_storage_component_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ssd_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_drive_type',
            field=models.CharField(blank=True, max_length=30, verbose_name='Тип накопичувача'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_component_capacity',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм SSD накопичувача'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_flash_type',
            field=models.CharField(blank=True, max_length=40, verbose_name='Тип флеш-пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_form_factor',
            field=models.CharField(blank=True, max_length=30, verbose_name='Форм-фактор SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_m2_size',
            field=models.CharField(blank=True, max_length=30, verbose_name='Типорозмір M.2'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_interface',
            field=models.CharField(blank=True, max_length=50, verbose_name='Інтерфейс підключення SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_read_speed',
            field=models.CharField(blank=True, max_length=40, verbose_name='Швидкість читання SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_write_speed',
            field=models.CharField(blank=True, max_length=40, verbose_name='Швидкість запису SSD'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_thickness',
            field=models.CharField(blank=True, max_length=30, verbose_name='Товщина SSD'),
        ),
        migrations.RunPython(copy_existing_ssd_capacity, migrations.RunPython.noop),
    ]
