from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0051_add_thermal_paste_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='peripheral_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('keyboard', 'Клавіатури'),
                    ('mouse', 'Мишки'),
                    ('mouse_pad', 'Килимки'),
                ],
                max_length=20,
                verbose_name='Тип периферії',
            ),
        ),
    ]
