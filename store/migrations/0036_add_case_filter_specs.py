from django.db import migrations, models


def copy_existing_case_specs(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    for product in Product.objects.using(database).filter(component_type='case').iterator():
        updates = {}
        if not product.case_manufacturer:
            updates['case_manufacturer'] = product.computer_manufacturer or product.manufacturer
        if not product.case_color:
            updates['case_color'] = product.computer_color or product.color
        if updates:
            Product.objects.using(database).filter(pk=product.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0035_add_hdd_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='case_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_class',
            field=models.CharField(blank=True, max_length=40, verbose_name='Клас корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_form_factor',
            field=models.CharField(blank=True, max_length=40, verbose_name='Типорозмір корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_installation',
            field=models.CharField(blank=True, max_length=40, verbose_name='Спосіб встановлення корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_supported_motherboards',
            field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='Підтримувані материнські плати'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_psu_included',
            field=models.CharField(blank=True, max_length=40, verbose_name='Наявність блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_3_5_bays',
            field=models.CharField(blank=True, max_length=20, verbose_name='Кількість внутрішніх відсіків 3.5"'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_fan_configuration',
            field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='Кількість і розмір вентиляторів'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_external_connectors',
            field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='Зовнішні роз’єми корпусу'),
        ),
        migrations.AddField(
            model_name='product',
            name='case_color',
            field=models.CharField(blank=True, max_length=40, verbose_name='Колір корпусу'),
        ),
        migrations.RunPython(copy_existing_case_specs, migrations.RunPython.noop),
    ]
