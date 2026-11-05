from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0022_product_processor_detail_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cpu_country_of_origin',
            field=models.CharField(blank=True, max_length=100, verbose_name='Країна виробництва'),
        ),
        migrations.AddField(
            model_name='product',
            name='cpu_warranty_months',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Гарантія, міс.'),
        ),
    ]
