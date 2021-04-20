from django.db import models

# Create your models here.

class WarehouseStocks(models.Model):
    title = models.CharField(max_length=40, null=False)
    amount = models.FloatField(default=1)
    unit = models.CharField(max_length=20, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    date = models.DateField()


