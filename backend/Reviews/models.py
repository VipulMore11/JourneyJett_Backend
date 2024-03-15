from django.db import models
from Venues.models import Places

class Reviews(models.Model):
    place       = models.ForeignKey(Places, on_delete=models.CASCADE)
    review     = models.CharField(max_length=255, blank=True, null=True)
    rating      = models.PositiveIntegerField( null=True, blank=True)

    class Meta:
        db_table = 'reviews'
