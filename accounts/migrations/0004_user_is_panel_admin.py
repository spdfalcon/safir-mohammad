# Generated by Django 4.2.1 on 2024-02-19 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_verificationcode_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_panel_admin',
            field=models.BooleanField(default=False, verbose_name='دسترسی به پنل ادمین'),
        ),
    ]