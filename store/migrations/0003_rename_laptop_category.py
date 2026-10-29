from django.db import migrations


def rename_laptop_category(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias

    # Якщо існує категорія в однині, перейменовуємо її або зливаємо
    # з уже наявною категорією в множині, не втрачаючи товари.
    singular = Category.objects.using(database).filter(name='Ноутбук').first()
    if singular is None:
        return

    plural = Category.objects.using(database).filter(name='Ноутбуки').first()
    if plural is None:
        singular.name = 'Ноутбуки'
        singular.save(using=database, update_fields=['name'])
        return

    Product.objects.using(database).filter(category_id=singular.pk).update(
        category_id=plural.pk,
    )
    singular.delete(using=database)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0002_category'),
    ]

    operations = [
        migrations.RunPython(rename_laptop_category, migrations.RunPython.noop),
    ]
