from django.db import migrations, models


def split_existing_storage_products(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    for product in Product.objects.using(database).filter(component_type='storage').only(
        'pk',
        'name',
        'storage_types',
    ):
        description = f'{product.name} {product.storage_types}'.casefold()
        component_type = (
            'hdd'
            if any(marker in description for marker in ('hdd', 'жорстк', 'hard disk', 'hard drive'))
            else 'ssd'
        )
        Product.objects.using(database).filter(pk=product.pk).update(
            component_type=component_type,
        )


def merge_storage_component_types(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    Product.objects.using(database).filter(
        component_type__in=('ssd', 'hdd'),
    ).update(component_type='storage')


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0030_product_memory_detail_specs'),
    ]

    operations = [
        migrations.RunPython(
            split_existing_storage_products,
            merge_storage_component_types,
        ),
        migrations.AlterField(
            model_name='product',
            name='component_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('processor', 'Процесори'),
                    ('motherboard', 'Материнські плати'),
                    ('graphics_card', 'Відеокарти'),
                    ('memory', 'Оперативна пам’ять'),
                    ('ssd', 'SSD накопичувачі'),
                    ('hdd', 'Жорсткі диски HDD'),
                    ('case', 'Корпуси'),
                    ('power_supply', 'Блоки живлення'),
                    ('cooling', 'Системи охолодження'),
                ],
                max_length=30,
                verbose_name='Тип комплектуючого для ПК',
            ),
        ),
    ]
