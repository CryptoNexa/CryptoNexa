# Generated by Django 4.2.6 on 2023-11-25 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuySell', '0003_rename_total_spent_transaction_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_fee',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
        ),
    ]