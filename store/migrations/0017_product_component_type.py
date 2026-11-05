from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0016_separate_computer_filter_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='component_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('processor', 'Процесори'),
                    ('motherboard', 'Материнські плати'),
                    ('graphics_card', 'Відеокарти'),
                    ('memory', 'Оперативна пам’ять'),
                    ('storage', 'Накопичувачі SSD / HDD'),
                    ('case', 'Корпуси'),
                    ('power_supply', 'Блоки живлення'),
                    ('cooling', 'Системи охолодження'),
                ],
                max_length=30,
                verbose_name='Тип комплектуючого для ПК',
            ),
        ),
    ]
