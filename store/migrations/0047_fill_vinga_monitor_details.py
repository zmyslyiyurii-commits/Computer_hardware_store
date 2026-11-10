from django.db import migrations


def fill_vinga_monitor_details(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    monitors = Product.objects.filter(
        category__name__iexact='Монітори',
        name__icontains='24S110-11B',
    )
    defaults = {
        'manufacturer': 'Vinga',
        'country_of_origin': 'Китай',
        'warranty_months': 12,
        'color': 'чорний',
        'features': (
            'Виробник може змінювати властивості, характеристики, зовнішній вигляд '
            'і комплектацію товарів без попередження'
        ),
    }

    for product in monitors:
        updated_fields = []
        for field_name, value in defaults.items():
            if not getattr(product, field_name):
                setattr(product, field_name, value)
                updated_fields.append(field_name)
        if updated_fields:
            product.save(update_fields=updated_fields)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0046_add_monitor_detail_specs'),
    ]

    operations = [
        migrations.RunPython(
            fill_vinga_monitor_details,
            migrations.RunPython.noop,
        ),
    ]
