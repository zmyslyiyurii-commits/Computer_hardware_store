from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0027_product_video_card_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(
                default=False,
                help_text='Познач товар, якщо він має відображатися в блоці на головній сторінці.',
                verbose_name='Показувати в «Популярне зараз»',
            ),
        ),
    ]
