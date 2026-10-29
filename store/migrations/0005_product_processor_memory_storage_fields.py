from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0004_product_laptop_filter_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='intel_generation',
            field=models.CharField(blank=True, max_length=30, verbose_name='Покоління процесора Intel'),
        ),
        migrations.AddField(
            model_name='product',
            name='amd_generation',
            field=models.CharField(blank=True, max_length=30, verbose_name='Покоління процесора AMD'),
        ),
        migrations.AddField(
            model_name='product',
            name='processor',
            field=models.CharField(blank=True, max_length=100, verbose_name='Процесор'),
        ),
        migrations.AddField(
            model_name='product',
            name='processor_cores',
            field=models.CharField(blank=True, max_length=10, verbose_name='Кількість ядер процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='ram_type',
            field=models.CharField(blank=True, max_length=20, verbose_name="Тип оперативної пам'яті"),
        ),
        migrations.AddField(
            model_name='product',
            name='ram_capacity',
            field=models.CharField(blank=True, max_length=20, verbose_name="Об'єм оперативної пам'яті"),
        ),
        migrations.AddField(
            model_name='product',
            name='ram_slots',
            field=models.CharField(blank=True, max_length=50, verbose_name='Кількість слотів для оперативної пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='ssd_capacity',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм SSD'),
        ),
    ]
