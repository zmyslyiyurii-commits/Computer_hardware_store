from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0026_product_video_card_specs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='video_card_manufacturer',
            field=models.CharField(blank=True, max_length=100, verbose_name='Виробник'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_boost_clock',
            field=models.CharField(blank=True, max_length=30, verbose_name='Частота ядра (Boost)'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_memory_frequency',
            field=models.CharField(blank=True, max_length=30, verbose_name='Частота пам’яті'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_max_displays',
            field=models.CharField(blank=True, max_length=20, verbose_name='Максимальне число дисплеїв'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_max_resolution',
            field=models.CharField(blank=True, max_length=50, verbose_name='Максимальна роздільна здатність'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_hdcp',
            field=models.CharField(blank=True, max_length=20, verbose_name='Сумісність з HDCP'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_recommended_psu',
            field=models.CharField(blank=True, max_length=30, verbose_name='Мінімальна рекомендована потужність блоку живлення'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_directx',
            field=models.CharField(blank=True, max_length=30, verbose_name='Версія DirectX'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_opengl',
            field=models.CharField(blank=True, max_length=30, verbose_name='Версія OpenGL'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_dlss',
            field=models.CharField(blank=True, max_length=50, verbose_name='Версія DLSS'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_dimensions',
            field=models.CharField(blank=True, max_length=50, verbose_name='Розміри'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_weight',
            field=models.CharField(blank=True, max_length=30, verbose_name='Вага'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія, міс.'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_barcode',
            field=models.CharField(blank=True, max_length=80, verbose_name='Штрихкод'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_card_note',
            field=models.TextField(blank=True, verbose_name='Примітка'),
        ),
    ]
