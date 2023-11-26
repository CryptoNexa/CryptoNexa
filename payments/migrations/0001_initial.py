# Generated by Django 4.2.6 on 2023-11-26 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("BuySell", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPaymentSell",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_status", models.BooleanField(default=False)),
                (
                    "account_holder_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "account_number",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                (
                    "transit_number",
                    models.CharField(blank=True, max_length=9, null=True),
                ),
                (
                    "routing_number",
                    models.CharField(blank=True, max_length=9, null=True),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=4, max_digits=10, null=True
                    ),
                ),
                (
                    "transaction_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="BuySell.transaction",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserPaymentBuy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_status", models.BooleanField(default=False)),
                ("stripe_id", models.CharField(default="", max_length=255)),
                (
                    "transaction_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="BuySell.transaction",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
