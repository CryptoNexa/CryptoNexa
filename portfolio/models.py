from django.db import models
from core.models import User, Cryptocurrency
from BuySell.models import Transaction


class portfolio(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Cryptocurrency= models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    Transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


