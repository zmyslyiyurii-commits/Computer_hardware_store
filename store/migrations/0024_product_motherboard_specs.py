from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0023_product_processor_country_warranty'),
    ]

    operations = [
        migrations.AddField(model_name='product', name='motherboard_manufacturer', field=models.CharField(blank=True, max_length=100, verbose_name='Виробник материнської плати')),
        migrations.AddField(model_name='product', name='motherboard_available_today', field=models.BooleanField(default=False, verbose_name='Можна отримати сьогодні')),
        migrations.AddField(model_name='product', name='motherboard_purpose', field=models.CharField(blank=True, max_length=50, verbose_name='Призначення материнської плати')),
        migrations.AddField(model_name='product', name='motherboard_product_socket', field=models.CharField(blank=True, max_length=40, verbose_name='Сокет материнської плати')),
        migrations.AddField(model_name='product', name='motherboard_pcie_x1_slots', field=models.CharField(blank=True, max_length=30, verbose_name='PCI Express x1')),
        migrations.AddField(model_name='product', name='motherboard_pcie_x4_slots', field=models.CharField(blank=True, max_length=30, verbose_name='PCI Express x4')),
        migrations.AddField(model_name='product', name='motherboard_pcie_x16_slots', field=models.CharField(blank=True, max_length=30, verbose_name='PCI Express x16')),
        migrations.AddField(model_name='product', name='motherboard_pci_slots', field=models.CharField(blank=True, max_length=30, verbose_name='Слоти PCI')),
        migrations.AddField(model_name='product', name='motherboard_chipset_model', field=models.CharField(blank=True, max_length=100, verbose_name='Модель чипсета')),
        migrations.AddField(model_name='product', name='motherboard_ram_type', field=models.CharField(blank=True, max_length=40, verbose_name='Тип оперативної пам’яті материнської плати')),
        migrations.AddField(model_name='product', name='motherboard_ram_slots', field=models.CharField(blank=True, max_length=30, verbose_name='Кількість роз’ємів оперативної пам’яті')),
        migrations.AddField(model_name='product', name='motherboard_max_ram', field=models.CharField(blank=True, max_length=30, verbose_name='Максимальний об’єм оперативної пам’яті')),
        migrations.AddField(model_name='product', name='motherboard_max_ram_frequency', field=models.CharField(blank=True, max_length=30, verbose_name='Максимальна частота оперативної пам’яті')),
        migrations.AddField(model_name='product', name='motherboard_integrated_video', field=models.CharField(blank=True, max_length=80, verbose_name='Вбудоване відео')),
        migrations.AddField(model_name='product', name='motherboard_lan_speed', field=models.CharField(blank=True, max_length=30, verbose_name='Швидкість LAN портів')),
        migrations.AddField(model_name='product', name='motherboard_video_outputs', field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='Відеовиходи')),
        migrations.AddField(model_name='product', name='motherboard_usb', field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='USB')),
        migrations.AddField(model_name='product', name='motherboard_digital_audio_output', field=models.CharField(blank=True, max_length=100, verbose_name='Цифровий аудіо роз’єм (S/PDIF)')),
        migrations.AddField(model_name='product', name='motherboard_m2_slots', field=models.CharField(blank=True, max_length=30, verbose_name='Кількість роз’ємів M.2')),
        migrations.AddField(model_name='product', name='motherboard_sata3_ports', field=models.CharField(blank=True, max_length=30, verbose_name='Кількість SATA-III портів')),
        migrations.AddField(model_name='product', name='motherboard_satae_slot', field=models.CharField(blank=True, max_length=50, verbose_name='SATAe роз’єм')),
        migrations.AddField(model_name='product', name='motherboard_u2_slot', field=models.CharField(blank=True, max_length=50, verbose_name='U.2 роз’єм')),
        migrations.AddField(model_name='product', name='motherboard_wireless', field=models.TextField(blank=True, help_text='Якщо значень кілька, розділяйте їх комами.', verbose_name='Бездротовий зв’язок материнської плати')),
        migrations.AddField(model_name='product', name='motherboard_raid_controller', field=models.CharField(blank=True, max_length=50, verbose_name='Контролер RAID')),
        migrations.AddField(model_name='product', name='motherboard_search_tag', field=models.CharField(blank=True, max_length=100, verbose_name='Також шукають')),
        migrations.AddField(model_name='product', name='motherboard_form_factor', field=models.CharField(blank=True, max_length=50, verbose_name='Форм-фактор материнської плати')),
    ]
