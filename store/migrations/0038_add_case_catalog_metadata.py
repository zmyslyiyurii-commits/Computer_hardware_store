from django.db import migrations, models


def copy_existing_case_metadata(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    for product in Product.objects.using(database).filter(component_type='case').iterator():
        updates = {}
        if not product.case_country_of_origin:
            updates['case_country_of_origin'] = product.computer_country_of_origin or product.country_of_origin
        if product.case_warranty_months is None:
            updates['case_warranty_months'] = (
                product.computer_warranty_months
                if product.computer_warranty_months is not None
                else product.warranty_months
            )
        if not product.case_note:
            updates['case_note'] = product.computer_features or product.features
        if updates:
            Product.objects.using(database).filter(pk=product.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0037_add_case_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='case_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія корпусу, міс.'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_note',
            field=models.TextField(blank=True, verbose_name='Примітка до корпусу'),
        ),
        migrations.RunPython(copy_existing_case_metadata, migrations.RunPython.noop),
    ]
