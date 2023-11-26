from django.db import models

from datetime import datetime
from core.models import User


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    type = models.CharField(max_length=4, default="buy")
    coin = models.CharField(max_length=30)
    currency = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    price = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    total_spent = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    datetime = models.DateTimeField()
    transaction_fee = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    notes = models.TextField(help_text="Please add your notes here", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')

    def __str__(self):
        # return f'{self.id}'
        return f'{self.id} - {self.type} - {self.coin} - {self.user}'