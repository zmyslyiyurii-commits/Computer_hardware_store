from django.db import migrations, models


def copy_existing_power_supply_specs(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    for product in Product.objects.using(database).filter(component_type='power_supply').iterator():
        updates = {}
        if not product.psu_manufacturer and product.manufacturer:
            updates['psu_manufacturer'] = product.manufacturer
        if not product.psu_wattage and product.psu_power:
            updates['psu_wattage'] = product.psu_power
        if updates:
            Product.objects.using(database).filter(pk=product.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0038_add_case_catalog_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='psu_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_type',
            field=models.CharField(blank=True, max_length=60, verbose_name='Тип блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_standard',
            field=models.CharField(blank=True, max_length=40, verbose_name='Стандарт блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_wattage',
            field=models.CharField(blank=True, max_length=30, verbose_name='Потужність блоку живлення, Вт'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_modular_connection',
            field=models.CharField(blank=True, max_length=30, verbose_name='Модульне підключення кабелів'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_certification',
            field=models.CharField(blank=True, max_length=40, verbose_name='Сертифікація 80 PLUS'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_pfc',
            field=models.CharField(blank=True, max_length=30, verbose_name='Модуль PFC'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_pcie_connectors',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість роз’ємів додаткового живлення для відеокарт'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_sata_connectors',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість роз’ємів SATA'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_fan_diameter',
            field=models.CharField(blank=True, max_length=30, verbose_name='Діаметр вентилятора блоку живлення'),
        ),
        migrations.RunPython(copy_existing_power_supply_specs, migrations.RunPython.noop),
    ]
