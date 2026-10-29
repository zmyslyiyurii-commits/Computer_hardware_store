from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0005_product_processor_memory_storage_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='graphics_type',
            field=models.CharField(blank=True, max_length=30, verbose_name='Тип відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='discrete_graphics_series',
            field=models.CharField(blank=True, max_length=100, verbose_name='Серія дискретної відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_memory',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм відеопам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='wireless_technologies',
            field=models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Бездротові технології',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='interfaces',
            field=models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Інтерфейси та підключення',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='operating_system',
            field=models.CharField(blank=True, max_length=100, verbose_name='Операційна система'),
        ),
        migrations.AddField(
            model_name='product',
            name='battery_capacity',
            field=models.CharField(blank=True, max_length=40, verbose_name='Ємність акумулятора'),
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Особливості',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(blank=True, max_length=30, verbose_name='Вага'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=30, verbose_name='Колір'),
        ),
    ]
