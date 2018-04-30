from django.db import models

# Create your models here.
class Region(models.Model):
    region_code = models.CharField(max_length=10)
    city_name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=10)

class Forecast(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    temperture = models.CharField(max_length=10)
    wind = models.CharField(max_length=10)
    wind_angle = models.CharField(max_length=10)
    pub_date = models.DateTimeField('date published')

class Alert(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    