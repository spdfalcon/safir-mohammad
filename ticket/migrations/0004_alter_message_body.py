# Generated by Django 4.2.1 on 2024-02-19 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_alter_message_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(verbose_name='متن پیام'),
        ),
    ]
