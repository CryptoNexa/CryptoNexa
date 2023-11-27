
from django.db import models
from core.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from BuySell.models import Transaction


class UserPaymentBuy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    stripe_id = models.CharField(max_length=255,default='')


class UserPaymentSell(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=30)
    transit_number = models.CharField(max_length=9)  # Canada
    routing_number = models.CharField(max_length=9)  # USA
    amount = models.DecimalField(max_digits=10, decimal_places=4)
