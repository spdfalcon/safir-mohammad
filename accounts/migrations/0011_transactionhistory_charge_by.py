# Generated by Django 4.2.1 on 2024-06-29 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_wallet_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='charge_by',
            field=models.CharField(choices=[('A', 'ادمین'), ('U', 'کاربر')], default='A', max_length=10),
        ),
    ]