from django.db import migrations


OLD_NAME = 'Мережеве обладнання'
NEW_NAME = 'Мережеві фільтри та подовжувачі'


def rename_network_category(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    old_category = Category.objects.using(database).filter(name=OLD_NAME).first()
    if old_category is None:
        return

    new_category = Category.objects.using(database).filter(name=NEW_NAME).first()
    if new_category is None:
        Category.objects.using(database).filter(pk=old_category.pk).update(name=NEW_NAME)
        return

    if not new_category.icon and old_category.icon:
        Category.objects.using(database).filter(pk=new_category.pk).update(icon=old_category.icon)
    Product.objects.using(database).filter(category_id=old_category.pk).update(
        category_id=new_category.pk,
    )
    old_category.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0043_add_cooling_detail_specs'),
    ]

    operations = [
        migrations.RunPython(rename_network_category, migrations.RunPython.noop),
    ]
