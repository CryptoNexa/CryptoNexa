# models.py
from django.db import models
from core.models import User
from BuySell.models import Transaction
from django.utils import timezone


def user_issue_files_upload_path(instance, filename):
    # Upload files to a user-specific subdirectory in support_files
    return f'support_files/user_{instance.user.id}/{filename}'


class SupportIssue(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ]
    ISSUE_TYPES = [
        ('currency_exchange', 'Currency Exchange'),
        ('buy_sell_orders', 'Buy/Sell Orders'),
        ('portfolio', 'Portfolio'),
        ('purchase', 'Purchase'),
        ('unauthorized_charge', 'Unauthorized Charge'),
        ('refunds', 'Refunds'),
        ('other', 'Other')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES, default='other')
    issue_title = models.CharField(max_length=255)
    issue_description = models.TextField()
    transaction_id = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    files = models.FileField(upload_to=user_issue_files_upload_path, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"{self.id} - {self.issue_title} - {self.get_status_display()} - {self.issue_type}"
