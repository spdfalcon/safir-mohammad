# Generated by Django 4.2.1 on 2024-02-18 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price_after_discount',
            field=models.PositiveBigIntegerField(default=1, verbose_name='قیمت بعد از تخفیف'),
            preserve_default=False,
        ),
    ]