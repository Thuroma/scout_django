from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Search(models.Model):
#     user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     date_searched = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return f'{self.pk}: {self.name} is at lat: {self.latitude}, long: {self.longitude}. Searched on {self.date_searched}.'

class Search(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=50)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    street_address = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=50)
    zip_code = models.IntegerField(blank=True, null=True)
    date_searched = models.DateField(auto_now=True)
    is_bookmarked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}: {self.name} is at lat: {self.latitude}, long: {self.longitude}, street: {self.street_address}, city: {self.city}, state: {self.state}, zip: {self.zip_code}. Searched on {self.date_searched}.'