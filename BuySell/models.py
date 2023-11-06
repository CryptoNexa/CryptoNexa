from django.db import models

from datetime import datetime
from core.models import User


class Transaction(models.Model):
    type = models.CharField(max_length=4, default="buy")
    coin = models.CharField(max_length=30)
    currency = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    datetime = models.DateTimeField()
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(help_text="Please add your notes here")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # payment_details = models.ForeignKey(Payment, on_delete=models.CASCADE())

    def __str__(self):
        return f'{self.type} - {self.coin} - {self.user}'