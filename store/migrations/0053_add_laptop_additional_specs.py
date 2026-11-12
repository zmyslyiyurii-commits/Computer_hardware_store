from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0052_add_peripheral_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ssd_m2_slots',
            field=models.CharField(
                blank=True,
                max_length=20,
                verbose_name='Кількість слотів M.2',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='laptop_barcode',
            field=models.CharField(
                blank=True,
                max_length=80,
                verbose_name='Штрихкод ноутбука',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='laptop_note',
            field=models.TextField(blank=True, verbose_name='Примітка до ноутбука'),
        ),
        migrations.AlterField(
            model_name='product',
            name='storage_types',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='Тип накопичувача',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='audio_controller',
            field=models.CharField(
                blank=True,
                max_length=150,
                verbose_name='Аудіосистема',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='wired_network',
            field=models.CharField(
                blank=True,
                max_length=80,
                verbose_name='Мережевий адаптер',
            ),
        ),
    ]
