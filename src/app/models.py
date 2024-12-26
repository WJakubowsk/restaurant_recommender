from django.db import models


# TODO to be developed further
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    cuisine = models.CharField(max_length=50)
    rating = models.FloatField()
