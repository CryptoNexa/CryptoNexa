# Generated by Django 4.2.6 on 2023-11-29 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BuySell', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cryptocurrency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cryptocurrency')),
                ('Transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BuySell.transaction')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]