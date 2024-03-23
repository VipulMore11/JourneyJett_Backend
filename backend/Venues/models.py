from django.db import models
from Authentication.models import Profile

class Places(models.Model):
    CAT_CHOICES = [
        ('Adventure', 'Adventure'),
        ('Heritage', 'Heritage'),
        ('Pilgrimage', 'Pilgrimage'),
        ('Beach', 'Beach'),
        ('trending', 'trending'),
    ]
    name = models.CharField(max_length=200, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    city =models.CharField(max_length=200,blank=True,null=True)
    state =models.CharField(max_length=200,blank=True,null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    best_time = models.CharField(max_length=200, blank=True, null=True)
    rating = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(choices=CAT_CHOICES, max_length=20,default='',blank=True, null=True)

    class Meta:
        db_table = 'places'

class Festivals(models.Model):
    festivals = models.ForeignKey(Places, related_name='festivals' ,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'festivals'

class PlacesImage(models.Model):
    place = models.ForeignKey(Places, related_name='images', on_delete=models.CASCADE)
    places_image = models.ImageField(upload_to='places/',blank=True, null=True)#

    class Meta:
        db_table ='places_images'

class UserVisits(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table ='user_visits'

class SavedPlaces(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

    class Meta:
        db_table ='saved_places'
        unique_together = ('user', 'place')