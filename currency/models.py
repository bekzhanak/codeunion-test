from django.db import models


# Create your models here.
class Currency(models.Model):
    """DB model to represent the current exchange rates in relation to the KZT.
    """
    name = models.CharField(max_length=256, unique=True)
    rate = models.FloatField()

    class Meta:
        db_table = "currency"
