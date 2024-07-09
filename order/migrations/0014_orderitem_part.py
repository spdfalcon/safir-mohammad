# Generated by Django 4.2.1 on 2024-05-09 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_part_price'),
        ('order', '0013_alter_order_options_order_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='products.part', verbose_name='محصول مربوطه'),
        ),
    ]