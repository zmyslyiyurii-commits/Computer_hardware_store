from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0021_product_processor_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cpu_process_technology',
            field=models.CharField(blank=True, max_length=30, verbose_name='Техпроцес'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_l1_cache',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм кеш-пам’яті 1-го рівня'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_l2_cache',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм кеш-пам’яті 2-го рівня'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_l3_cache',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм кеш-пам’яті 3-го рівня'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_max_memory',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальний обсяг оперативної пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_memory_type',
            field=models.CharField(blank=True, max_length=30, verbose_name='Тип оперативної пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_max_memory_speed',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальна швидкість пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_memory_channels',
            field=models.CharField(blank=True, max_length=20, verbose_name='Кількість каналів пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_max_temperature',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимально допустима температура'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_unlocked_multiplier',
            field=models.CharField(blank=True, max_length=20, verbose_name='Розблокований множник'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_pcie_version',
            field=models.CharField(blank=True, max_length=20, verbose_name='Версія PCI Express'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_release_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата виходу'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_note',
            field=models.TextField(blank=True, verbose_name='Примітка до процесора'),
        ),
    ]
