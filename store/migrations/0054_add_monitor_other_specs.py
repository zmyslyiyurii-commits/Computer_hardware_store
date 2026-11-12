from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0053_add_laptop_additional_specs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='ssd_m2_slots',
        ),
        migrations.RemoveField(
            model_name='product',
            name='laptop_barcode',
        ),
        migrations.RemoveField(
            model_name='product',
            name='laptop_note',
        ),
        migrations.AlterField(
            model_name='product',
            name='storage_types',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='Типи внутрішніх накопичувачів',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='audio_controller',
            field=models.CharField(
                blank=True,
                max_length=150,
                verbose_name='Аудіоконтролер',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='wired_network',
            field=models.CharField(
                blank=True,
                max_length=80,
                verbose_name='Провідна мережа (LAN)',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_barcode',
            field=models.CharField(
                blank=True,
                max_length=80,
                verbose_name='Штрихкод монітора',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='monitor_note',
            field=models.TextField(
                blank=True,
                verbose_name='Примітка до монітора',
            ),
        ),
    ]
