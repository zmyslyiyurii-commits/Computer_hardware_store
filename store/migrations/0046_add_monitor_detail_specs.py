from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0045_add_monitor_filter_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='monitor_display_type',
            field=models.CharField(blank=True, max_length=100, verbose_name='Тип монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_brightness',
            field=models.CharField(blank=True, max_length=30, verbose_name='Яскравість монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_static_contrast',
            field=models.CharField(blank=True, max_length=30, verbose_name='Статична контрастність монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_dynamic_contrast',
            field=models.CharField(blank=True, max_length=30, verbose_name='Динамічна контрастність монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_viewing_angles',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кути огляду монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_max_colors',
            field=models.CharField(blank=True, max_length=30, verbose_name='Максимальна кількість кольорів монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_image_enhancement',
            field=models.TextField(blank=True, verbose_name='Технології покращення зображення монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_sync_technology',
            field=models.CharField(blank=True, max_length=100, verbose_name='Технології синхронізації монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_tilt_angle',
            field=models.CharField(blank=True, max_length=50, verbose_name='Регулювання нахилу монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_power_consumption',
            field=models.CharField(blank=True, max_length=30, verbose_name='Споживана потужність монітора в робочому режимі'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_standby_power',
            field=models.CharField(blank=True, max_length=30, verbose_name='Споживана потужність монітора в режимі очікування'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_dimensions_with_stand',
            field=models.CharField(blank=True, max_length=60, verbose_name='Розміри монітора з підставкою'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_dimensions_without_stand',
            field=models.CharField(blank=True, max_length=60, verbose_name='Розміри монітора без підставки'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_weight_unboxed',
            field=models.CharField(blank=True, max_length=30, verbose_name='Вага монітора без упаковки'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_weight_boxed',
            field=models.CharField(blank=True, max_length=30, verbose_name='Вага монітора з упаковкою'),
        ),
    ]
