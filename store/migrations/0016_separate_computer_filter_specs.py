from django.db import migrations, models


COMPUTER_FIELD_MAPPINGS = {
    'computer_processor_frequency': 'processor_frequency',
    'computer_storage_types': 'storage_types',
    'computer_hdd_capacity': 'hdd_capacity',
    'computer_optical_drive': 'optical_drive',
    'computer_card_reader': 'card_reader',
    'computer_built_in_microphone': 'built_in_microphone',
    'computer_built_in_speakers': 'built_in_speakers',
    'computer_audio_controller': 'audio_controller',
    'computer_multichannel_audio': 'multichannel_audio',
    'computer_wired_network': 'wired_network',
    'computer_peripherals_included': 'peripherals_included',
}


def copy_existing_computer_filter_specs(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    database = schema_editor.connection.alias
    computer_products = Product.objects.using(database).filter(
        category__name__iexact='Комп’ютери',
    )
    for product in computer_products.iterator():
        updates = {
            computer_field: getattr(product, source_field)
            for computer_field, source_field in COMPUTER_FIELD_MAPPINGS.items()
            if not getattr(product, computer_field)
        }
        if updates:
            Product.objects.using(database).filter(pk=product.pk).update(**updates)


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0015_computer_product_filters'),
    ]

    operations = [
        migrations.AddField('product', 'computer_processor_frequency', models.CharField(blank=True, max_length=30, verbose_name='Частота процесора, ГГц')),
        migrations.AddField('product', 'computer_storage_types', models.CharField(blank=True, max_length=100, verbose_name='Типи внутрішніх накопичувачів')),
        migrations.AddField('product', 'computer_hdd_capacity', models.CharField(blank=True, max_length=40, verbose_name='Об’єм HDD')),
        migrations.AddField('product', 'computer_optical_drive', models.CharField(blank=True, max_length=60, verbose_name='Оптичний привід')),
        migrations.AddField('product', 'computer_card_reader', models.CharField(blank=True, max_length=60, verbose_name='Кардридер')),
        migrations.AddField('product', 'computer_built_in_microphone', models.CharField(blank=True, max_length=60, verbose_name='Вбудований мікрофон')),
        migrations.AddField('product', 'computer_built_in_speakers', models.CharField(blank=True, max_length=60, verbose_name='Вбудовані динаміки')),
        migrations.AddField('product', 'computer_audio_controller', models.CharField(blank=True, max_length=150, verbose_name='Аудіоконтролер')),
        migrations.AddField('product', 'computer_multichannel_audio', models.CharField(blank=True, max_length=40, verbose_name='Багатоканальний звук')),
        migrations.AddField('product', 'computer_wired_network', models.CharField(blank=True, max_length=80, verbose_name='Провідна мережа (LAN)')),
        migrations.AddField('product', 'computer_peripherals_included', models.CharField(blank=True, max_length=150, verbose_name='Пристрої введення в комплекті')),
        migrations.AlterField(
            'product',
            'computer_wireless_technologies',
            models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Бездротові технології',
            ),
        ),
        migrations.AlterField(
            'product',
            'computer_interfaces',
            models.TextField(
                blank=True,
                help_text='Якщо значень кілька, розділяйте їх комами.',
                verbose_name='Зовнішні порти та роз’єми',
            ),
        ),
        migrations.RunPython(copy_existing_computer_filter_specs, migrations.RunPython.noop),
    ]
