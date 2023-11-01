from django.db import models


# Create your models here.
class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=100)
    symbol = models.CharField(max_length=2)

    def __str__(self):
        return self.name
