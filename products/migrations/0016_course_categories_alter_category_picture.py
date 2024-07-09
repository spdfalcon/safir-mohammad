# Generated by Django 4.2.1 on 2024-03-14 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_package_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='courses', to='products.category', verbose_name='دسته\u200cها'),
        ),
        migrations.AlterField(
            model_name='category',
            name='picture',
            field=models.ImageField(upload_to='category_images/', verbose_name='عکس گروه محصول'),
        ),
    ]