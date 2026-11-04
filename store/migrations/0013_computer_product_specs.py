from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0012_customer_profile_order_user'),
    ]

    operations = [
        migrations.AddField('product', 'computer_type', models.CharField(blank=True, max_length=60, verbose_name='Тип ПК')),
        migrations.AddField('product', 'computer_view', models.CharField(blank=True, max_length=60, verbose_name='Вид комп’ютера')),
        migrations.AddField('product', 'processor_threads', models.CharField(blank=True, max_length=20, verbose_name='Кількість потоків')),
        migrations.AddField('product', 'processor_frequency', models.CharField(blank=True, max_length=30, verbose_name='Частота процесора, ГГц')),
        migrations.AddField('product', 'processor_boost_frequency', models.CharField(blank=True, max_length=30, verbose_name='Частота в Boost, ГГц')),
        migrations.AddField('product', 'processor_boost_supported', models.CharField(blank=True, max_length=30, verbose_name='Підтримка Boost режиму')),
        migrations.AddField('product', 'motherboard_socket', models.CharField(blank=True, max_length=40, verbose_name='Сокет')),
        migrations.AddField('product', 'motherboard_chipset', models.CharField(blank=True, max_length=100, verbose_name='Чипсет')),
        migrations.AddField('product', 'graphics_card_manufacturer', models.CharField(blank=True, max_length=100, verbose_name='Виробник чипу відеокарти')),
        migrations.AddField('product', 'ram_form_factor', models.CharField(blank=True, max_length=40, verbose_name='Форм-фактор пам’яті')),
        migrations.AddField('product', 'ram_frequency', models.CharField(blank=True, max_length=40, verbose_name='Частота пам’яті')),
        migrations.AddField('product', 'ram_standard', models.CharField(blank=True, max_length=40, verbose_name='Стандарт пам’яті')),
        migrations.AddField('product', 'ram_max_capacity', models.CharField(blank=True, max_length=40, verbose_name='Максимальний об’єм пам’яті')),
        migrations.AddField('product', 'storage_types', models.CharField(blank=True, max_length=100, verbose_name='Типи внутрішніх накопичувачів')),
        migrations.AddField('product', 'hdd_capacity', models.CharField(blank=True, max_length=40, verbose_name='Об’єм HDD')),
        migrations.AddField('product', 'optical_drive', models.CharField(blank=True, max_length=60, verbose_name='Оптичний привід')),
        migrations.AddField('product', 'card_reader', models.CharField(blank=True, max_length=60, verbose_name='Кардридер')),
        migrations.AddField('product', 'built_in_microphone', models.CharField(blank=True, max_length=60, verbose_name='Вбудований мікрофон')),
        migrations.AddField('product', 'built_in_speakers', models.CharField(blank=True, max_length=60, verbose_name='Вбудовані динаміки')),
        migrations.AddField('product', 'audio_controller', models.CharField(blank=True, max_length=150, verbose_name='Аудіоконтролер')),
        migrations.AddField('product', 'multichannel_audio', models.CharField(blank=True, max_length=40, verbose_name='Багатоканальний звук')),
        migrations.AddField('product', 'wired_network', models.CharField(blank=True, max_length=80, verbose_name='Провідна мережа (LAN)')),
        migrations.AddField('product', 'peripherals_included', models.CharField(blank=True, max_length=150, verbose_name='Пристрої введення в комплекті')),
        migrations.AddField('product', 'case_model', models.CharField(blank=True, max_length=100, verbose_name='Модель корпусу')),
        migrations.AddField('product', 'case_metal_thickness', models.CharField(blank=True, max_length=40, verbose_name='Товщина металу корпусу')),
        migrations.AddField('product', 'case_material', models.CharField(blank=True, max_length=100, verbose_name='Матеріал корпусу')),
        migrations.AddField('product', 'psu_location', models.CharField(blank=True, max_length=60, verbose_name='Розташування блоку живлення')),
        migrations.AddField('product', 'psu_power', models.CharField(blank=True, max_length=40, verbose_name='Потужність блоку живлення')),
        migrations.AddField('product', 'case_lighting', models.CharField(blank=True, max_length=150, verbose_name='Підсвічування корпусу')),
        migrations.AddField('product', 'cooling', models.TextField(blank=True, verbose_name='Охолодження')),
    ]
