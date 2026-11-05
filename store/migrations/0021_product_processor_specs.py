from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0020_remove_maintenance_component_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cpu_manufacturer',
            field=models.CharField(blank=True, max_length=30, verbose_name='Виробник процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_family',
            field=models.CharField(blank=True, max_length=100, verbose_name='Сімейство процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_socket',
            field=models.CharField(blank=True, max_length=30, verbose_name='Сокет процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_core_count',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість ядер процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_thread_count',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість потоків процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_base_clock',
            field=models.CharField(blank=True, max_length=30, verbose_name='Базова тактова частота процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_max_clock',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальна тактова частота процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_tdp',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальний TDP процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_integrated_graphics',
            field=models.CharField(blank=True, max_length=100, verbose_name='Графічне ядро процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_intel_generation',
            field=models.CharField(blank=True, max_length=100, verbose_name='Покоління процесорів Intel'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_amd_architecture',
            field=models.CharField(blank=True, max_length=50, verbose_name='Архітектура ядра AMD'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_package_type',
            field=models.CharField(blank=True, max_length=40, verbose_name='Тип поставки процесора'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_cooling_included',
            field=models.CharField(blank=True, max_length=40, verbose_name='Охолодження в комплекті'),
        ),
    ]
