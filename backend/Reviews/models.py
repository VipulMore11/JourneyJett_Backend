from django.db import models
from Venues.models import Places
from Authentication.models import Profile

class Reviews(models.Model):
    place       = models.ForeignKey(Places, on_delete=models.CASCADE)
    review      = models.CharField(max_length=255, blank=True, null=True)
    rating      = models.PositiveIntegerField( null=True, blank=True)
    user        = models.ForeignKey(Profile, on_delete=models.CASCADE)
    class Meta:
        db_table = 'reviews'
        unique_together = ('user', 'place')