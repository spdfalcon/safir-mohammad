# Generated by Django 4.2.1 on 2024-03-11 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_comment_package_alter_comment_course_and_more'),
        ('order', '0008_order_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='course',
        ),
        migrations.RemoveField(
            model_name='order',
            name='package',
        ),
        migrations.AddField(
            model_name='order',
            name='ref_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='کد رهگیری پرداخت اینترنتی'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='products.course', verbose_name='مجموعه مربوطه')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='سفارش مربوطه')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='products.package', verbose_name='دسته بندی مربوطه')),
            ],
            options={
                'verbose_name': 'آیتم',
                'verbose_name_plural': 'آیتم ها',
            },
        ),
    ]
