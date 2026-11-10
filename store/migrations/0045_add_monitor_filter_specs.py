from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0044_rename_network_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='monitor_aspect_ratio',
            field=models.CharField(blank=True, max_length=20, verbose_name='Співвідношення сторін монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_backlight',
            field=models.CharField(blank=True, max_length=40, verbose_name='Підсвічування монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_response_time',
            field=models.CharField(blank=True, max_length=30, verbose_name='Час реакції матриці монітора'),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_stand_adjustment',
            field=models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Регулювання положення монітора',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_vesa',
            field=models.CharField(blank=True, max_length=40, verbose_name='Кріплення VESA монітора'),
        ),
    ]
