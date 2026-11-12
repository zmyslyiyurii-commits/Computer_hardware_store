from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0047_fill_vinga_monitor_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='network_product_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('мережевий розгалужувач', 'Мережевий розгалужувач'),
                    ('мережеві подовжувачі', 'Мережеві подовжувачі'),
                    ('мережеві фільтри живлення', 'Мережеві фільтри живлення'),
                ],
                max_length=80,
                verbose_name='Тип мережевого обладнання',
            ),
        ),
    ]
