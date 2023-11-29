# Generated by Django 4.2.6 on 2023-11-29 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import support.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BuySell', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_type', models.CharField(choices=[('currency_exchange', 'Currency Exchange'), ('buy_sell_orders', 'Buy/Sell Orders'), ('portfolio', 'Portfolio'), ('purchase', 'Purchase'), ('unauthorized_charge', 'Unauthorized Charge'), ('refunds', 'Refunds'), ('other', 'Other')], default='other', max_length=50)),
                ('issue_title', models.CharField(max_length=255)),
                ('issue_description', models.TextField()),
                ('files', models.FileField(blank=True, null=True, upload_to=support.models.user_issue_files_upload_path)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('in_progress', 'In Progress')], default='open', max_length=20)),
                ('transaction_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='BuySell.transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]