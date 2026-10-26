from django.db import migrations, models
import django.db.models.deletion


def copy_product_categories(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias

    for product in Product.objects.using(database).all().iterator():
        category, _ = Category.objects.using(database).get_or_create(
            name=product.category,
        )
        Product.objects.using(database).filter(pk=product.pk).update(
            category_ref_id=category.pk,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Назва')),
                ('icon', models.CharField(blank=True, max_length=8, verbose_name='Іконка')),
            ],
            options={
                'verbose_name': 'категорія',
                'verbose_name_plural': 'категорії',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category_ref',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='products',
                to='store.category',
                verbose_name='Категорія',
            ),
        ),
        migrations.RunPython(copy_product_categories, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category_ref',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='products',
                to='store.category',
                verbose_name='Категорія',
            ),
        ),
    ]
