from django.db import models


# Create your models here.

class Crypto(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(max_length=10)
    oneHourPrice = models.FloatField()
    oneHourFlag = models.FloatField()
    TwentyFourHour = models.FloatField()
    TwentyFourPrice = models.FloatField()
    MarketCap = models.IntegerField()
    Volume = models.IntegerField()

    def __str__(self):
        return self.name
