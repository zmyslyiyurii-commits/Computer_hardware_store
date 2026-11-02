import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0011_product_image_gallery'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Телефон')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'профіль покупця',
                'verbose_name_plural': 'профілі покупців',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store_orders', to=settings.AUTH_USER_MODEL, verbose_name='Акаунт покупця'),
        ),
    ]
