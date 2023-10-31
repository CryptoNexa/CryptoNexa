# Generated by Django 4.2.6 on 2023-10-31 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField(max_length=10)),
                ('oneHourPrice', models.FloatField()),
                ('oneHourFlag', models.FloatField()),
                ('TwentyFourHour', models.FloatField()),
                ('TwentyFourPrice', models.FloatField()),
                ('MarketCap', models.IntegerField(max_length=15)),
                ('Volume', models.IntegerField(max_length=15)),
            ],
        ),
    ]
