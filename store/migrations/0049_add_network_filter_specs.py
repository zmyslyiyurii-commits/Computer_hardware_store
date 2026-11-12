from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0048_add_network_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='network_socket_count',
            field=models.CharField(blank=True, max_length=20, verbose_name='Кількість розеток мережевого обладнання'),
        ),
        migrations.AddField(
            model_name='product',
            name='network_outlet_type',
            field=models.CharField(blank=True, max_length=100, verbose_name='Тип вихідних розеток мережевого обладнання'),
        ),
        migrations.AddField(
            model_name='product',
            name='network_input_plug_type',
            field=models.CharField(blank=True, max_length=100, verbose_name='Тип вхідної вилки мережевого обладнання'),
        ),
        migrations.AddField(
            model_name='product',
            name='network_usb_ports',
            field=models.CharField(blank=True, max_length=40, verbose_name='USB-порти мережевого обладнання'),
        ),
        migrations.AddField(
            model_name='product',
            name='network_cable_length',
            field=models.CharField(blank=True, max_length=30, verbose_name='Довжина кабелю мережевого обладнання'),
        ),
        migrations.AddField(
            model_name='product',
            name='network_features',
            field=models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Особливості мережевого обладнання',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_protection',
            field=models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Захист мережевого обладнання',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='network_total_power',
            field=models.CharField(blank=True, max_length=40, verbose_name='Сумарна потужність підключеного навантаження'),
        ),
    ]
