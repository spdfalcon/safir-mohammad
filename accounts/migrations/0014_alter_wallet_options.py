from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_transactionhistory_charge_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'verbose_name': 'کیف پول', 'verbose_name_plural': 'کیف های پول'},
        ),
    ]
