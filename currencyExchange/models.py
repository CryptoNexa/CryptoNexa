from django.db import models


# Create your models here.
class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
