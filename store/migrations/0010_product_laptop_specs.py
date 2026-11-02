from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0009_cart_reviews_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='model_series',
            field=models.CharField(blank=True, max_length=100, verbose_name='Серія (модельний ряд)'),
        ),
        migrations.AddField(
            model_name='product',
            name='webcam',
            field=models.CharField(blank=True, max_length=100, verbose_name='Веб-камера'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_features',
            field=models.TextField(blank=True, verbose_name='Додаткові можливості'),
        ),
        migrations.AddField(
            model_name='product',
            name='width',
            field=models.CharField(blank=True, max_length=30, verbose_name='Ширина, мм'),
        ),
        migrations.AddField(
            model_name='product',
            name='height',
            field=models.CharField(blank=True, max_length=30, verbose_name='Висота, мм'),
        ),
        migrations.AddField(
            model_name='product',
            name='depth',
            field=models.CharField(blank=True, max_length=30, verbose_name='Глибина, мм'),
        ),
        migrations.AddField(
            model_name='product',
            name='country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва'),
        ),
        migrations.AddField(
            model_name='product',
            name='warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія, міс.'),
        ),
    ]
