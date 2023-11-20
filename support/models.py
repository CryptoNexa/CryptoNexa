# models.py
from django.db import models
from core.models import User
from BuySell.models import Transaction


class SupportIssue(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_title = models.CharField(max_length=255)
    issue_description = models.TextField()
    transaction_id = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    files = models.FileField(upload_to='support_files/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"{self.id} - {self.issue_title} - {self.get_status_display()}"
