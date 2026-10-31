from django.db import migrations


CATEGORIES = (
    ('Комп’ютери', '⌘'),
    ('Комплектуючі для ПК', '⚙'),
    ('Монітори', '▣'),
    ('Периферія', '⌨'),
    ('Мережеве обладнання', '⌁'),
    ('Накопичувачі', '▤'),
    ('Аксесуари', '◉'),
)


def add_catalog_categories(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    database = schema_editor.connection.alias

    for name, icon in CATEGORIES:
        Category.objects.using(database).get_or_create(name=name, defaults={'icon': icon})


def remove_empty_catalog_categories(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    database = schema_editor.connection.alias

    Category.objects.using(database).filter(
        name__in=[name for name, _ in CATEGORIES],
        products__isnull=True,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0006_product_graphics_connectivity_fields'),
    ]

    operations = [
        migrations.RunPython(add_catalog_categories, remove_empty_catalog_categories),
    ]
