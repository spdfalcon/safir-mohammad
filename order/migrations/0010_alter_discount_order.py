# Generated by Django 4.2.1 on 2024-03-14 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_remove_order_course_remove_order_package_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='order',
            field=models.ManyToManyField(blank=True, null=True, related_name='order_discounts', to='order.order', verbose_name='سفارش'),
        ),
    ]