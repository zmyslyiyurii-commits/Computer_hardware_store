from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0049_add_network_filter_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='network_cable_specification',
            field=models.CharField(
                blank=True,
                max_length=80,
                verbose_name='Технічні характеристики кабелю мережевого обладнання',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_filter_material',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='Матеріал мережевого фільтра',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_additional_features',
            field=models.TextField(
                blank=True,
                verbose_name='Додаткові характеристики мережевого обладнання',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_nominal_voltage',
            field=models.CharField(
                blank=True,
                max_length=40,
                verbose_name='Номінальна напруга мережевого обладнання',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_breaker_trip_current',
            field=models.CharField(
                blank=True,
                max_length=30,
                verbose_name='Струм спрацьовування термозапобіжника мережевого обладнання',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_barcode',
            field=models.CharField(
                blank=True,
                max_length=80,
                verbose_name='Штрихкод мережевого обладнання',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_note',
            field=models.TextField(
                blank=True,
                verbose_name='Примітка до мережевого обладнання',
            ),
        ),
    ]
