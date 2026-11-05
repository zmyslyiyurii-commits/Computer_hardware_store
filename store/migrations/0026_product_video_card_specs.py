from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0025_product_motherboard_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='video_card_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_family',
            field=models.CharField(blank=True, max_length=50, verbose_name='Сімейство графіки'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_form_factor',
            field=models.CharField(blank=True, max_length=50, verbose_name='Форм-фактор відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_purpose',
            field=models.CharField(blank=True, max_length=50, verbose_name='Призначення відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_chip',
            field=models.CharField(blank=True, max_length=100, verbose_name='Графічний чип'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_interface',
            field=models.CharField(blank=True, max_length=50, verbose_name='Інтерфейс відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_memory_capacity',
            field=models.CharField(blank=True, max_length=30, verbose_name='Об’єм вбудованої пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_memory_type',
            field=models.CharField(blank=True, max_length=30, verbose_name='Тип пам’яті відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_memory_bus',
            field=models.CharField(blank=True, max_length=30, verbose_name='Розрядність шини пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_connectors',
            field=models.TextField(blank=True, verbose_name='Роз’єми відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_cooling_system',
            field=models.CharField(blank=True, max_length=50, verbose_name='Тип системи охолодження'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_cooling_type',
            field=models.CharField(blank=True, max_length=50, verbose_name='Вид охолодження відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_fan_count',
            field=models.CharField(blank=True, max_length=30, verbose_name='Кількість вентиляторів відеокарти'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_power_connectors',
            field=models.CharField(blank=True, max_length=50, verbose_name='Роз’єми додаткового живлення відеокарти'),
        ),
    ]
