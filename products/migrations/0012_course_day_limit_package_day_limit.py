# Generated by Django 4.2.1 on 2024-03-11 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_comment_package_alter_comment_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='day_limit',
            field=models.PositiveBigIntegerField(default=1, verbose_name='تعداد روز های قابل استفاده'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='day_limit',
            field=models.PositiveBigIntegerField(default=1, verbose_name='تعداد روز های قابل استفاده'),
            preserve_default=False,
        ),
    ]