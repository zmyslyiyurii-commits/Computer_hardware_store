from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0007_add_catalog_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис'),
        ),
    ]
