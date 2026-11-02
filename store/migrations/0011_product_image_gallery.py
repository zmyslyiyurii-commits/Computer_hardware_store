from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0010_product_laptop_specs'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(help_text='Встав повне посилання на зображення, наприклад https://example.com/photo.jpg.', max_length=1000, verbose_name='URL додаткового фото')),
                ('alt_text', models.CharField(blank=True, max_length=200, verbose_name='Опис фото')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'фото товару',
                'verbose_name_plural': 'фотографії товару',
                'ordering': ('position', 'pk'),
            },
        ),
    ]
