# Generated by Django 4.2.1 on 2024-07-07 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0004_minimumcartcost'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='minimum_cart_cost',
            new_name='MinimumCartCost',
        ),
    ]