from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0024_product_motherboard_specs'),
    ]

    operations = [
        migrations.AddField(model_name='product', name='motherboard_supported_processors', field=models.TextField(blank=True, verbose_name='Підтримка процесорів')),
        migrations.AddField(model_name='product', name='motherboard_expansion_slots', field=models.TextField(blank=True, verbose_name='Слоти розширення')),
        migrations.AddField(model_name='product', name='motherboard_ram_frequencies', field=models.TextField(blank=True, verbose_name='Частота оперативної пам’яті')),
        migrations.AddField(model_name='product', name='motherboard_dual_channel_support', field=models.CharField(blank=True, max_length=20, verbose_name='Підтримка двоканального режиму')),
        migrations.AddField(model_name='product', name='motherboard_ecc_support', field=models.CharField(blank=True, max_length=20, verbose_name='Підтримка ECC')),
        migrations.AddField(model_name='product', name='motherboard_audio_controller', field=models.CharField(blank=True, max_length=100, verbose_name='Аудіоконтролер')),
        migrations.AddField(model_name='product', name='motherboard_multichannel_audio', field=models.CharField(blank=True, max_length=30, verbose_name='Багатоканальний звук')),
        migrations.AddField(model_name='product', name='motherboard_lan_port_count', field=models.CharField(blank=True, max_length=30, verbose_name='Кількість LAN портів')),
        migrations.AddField(model_name='product', name='motherboard_network_adapter', field=models.CharField(blank=True, max_length=100, verbose_name='Тип мережевої карти')),
        migrations.AddField(model_name='product', name='motherboard_rear_ports', field=models.TextField(blank=True, verbose_name='Зовнішні порти')),
        migrations.AddField(model_name='product', name='motherboard_internal_ports', field=models.TextField(blank=True, verbose_name='Внутрішні роз’єми і порти')),
        migrations.AddField(model_name='product', name='motherboard_power_connector', field=models.CharField(blank=True, max_length=100, verbose_name='Конектор живлення')),
        migrations.AddField(model_name='product', name='motherboard_headers', field=models.TextField(blank=True, verbose_name='Колодки')),
        migrations.AddField(model_name='product', name='motherboard_fan_headers', field=models.CharField(blank=True, max_length=50, verbose_name='4-pin для вентилятора')),
        migrations.AddField(model_name='product', name='motherboard_other_connectors', field=models.TextField(blank=True, verbose_name='Інші коннектори')),
        migrations.AddField(model_name='product', name='motherboard_bios_type', field=models.CharField(blank=True, max_length=150, verbose_name='Тип BIOS')),
        migrations.AddField(model_name='product', name='motherboard_operating_system', field=models.CharField(blank=True, max_length=100, verbose_name='Підтримка ОС')),
        migrations.AddField(model_name='product', name='motherboard_height', field=models.CharField(blank=True, max_length=30, verbose_name='Висота, мм')),
        migrations.AddField(model_name='product', name='motherboard_width', field=models.CharField(blank=True, max_length=30, verbose_name='Ширина, мм')),
        migrations.AddField(model_name='product', name='motherboard_country_of_origin', field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва')),
        migrations.AddField(model_name='product', name='motherboard_warranty_months', field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія, міс.')),
        migrations.AddField(model_name='product', name='motherboard_barcode', field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод')),
        migrations.AddField(model_name='product', name='motherboard_note', field=models.TextField(blank=True, verbose_name='Примітка')),
    ]
