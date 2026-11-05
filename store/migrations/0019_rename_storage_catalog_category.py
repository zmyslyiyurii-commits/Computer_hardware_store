from django.db import migrations


OLD_CATEGORY_NAME = 'Накопичувачі'
NEW_CATEGORY_NAME = 'Обслуговування ПК'


def rename_storage_catalog_category(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    database = schema_editor.connection.alias
    old_category = Category.objects.using(database).filter(name=OLD_CATEGORY_NAME).first()
    if not old_category:
        return

    if Category.objects.using(database).filter(name=NEW_CATEGORY_NAME).exists():
        raise RuntimeError(
            'Both catalog categories already exist. Merge or rename '
            f'"{OLD_CATEGORY_NAME}" and "{NEW_CATEGORY_NAME}" before migrating.'
        )

    old_category.name = NEW_CATEGORY_NAME
    old_category.icon = '⚙'
    old_category.save(using=database, update_fields=('name', 'icon'))


def restore_storage_catalog_category(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    database = schema_editor.connection.alias
    maintenance_category = Category.objects.using(database).filter(name=NEW_CATEGORY_NAME).first()
    if not maintenance_category:
        return

    if Category.objects.using(database).filter(name=OLD_CATEGORY_NAME).exists():
        raise RuntimeError(
            'Cannot reverse the catalog category rename because '
            f'"{OLD_CATEGORY_NAME}" already exists.'
        )

    maintenance_category.name = OLD_CATEGORY_NAME
    maintenance_category.icon = '▤'
    maintenance_category.save(using=database, update_fields=('name', 'icon'))


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0018_product_component_maintenance'),
    ]

    operations = [
        migrations.RunPython(
            rename_storage_catalog_category,
            restore_storage_catalog_category,
        ),
    ]
