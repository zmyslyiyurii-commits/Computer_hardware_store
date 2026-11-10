from django.db import migrations, models


def copy_power_supply_origin_and_warranty(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    for product in Product.objects.using(database).filter(component_type='power_supply').iterator():
        updates = {}
        if not product.psu_country_of_origin and product.country_of_origin:
            updates['psu_country_of_origin'] = product.country_of_origin
        if product.psu_warranty_months is None and product.warranty_months is not None:
            updates['psu_warranty_months'] = product.warranty_months
        if updates:
            Product.objects.using(database).filter(pk=product.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0040_add_power_supply_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='psu_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='psu_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія блоку живлення, міс.'),
        ),
        migrations.RunPython(copy_power_supply_origin_and_warranty, migrations.RunPython.noop),
    ]
