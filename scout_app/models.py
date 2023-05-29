from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Search(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_searched = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.pk}: {self.name} is at lat: {self.latitude}, long: {self.longitude}. Searched on {self.date_searched}.'
