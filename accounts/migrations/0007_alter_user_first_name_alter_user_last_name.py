# Generated by Django 4.2.1 on 2024-05-13 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=30, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=50, null=True, verbose_name='نام خانوادگی'),
        ),
    ]