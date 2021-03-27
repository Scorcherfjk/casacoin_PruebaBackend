from django.db import models


class Scraper(models.Model):

    currency = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    frequency = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    value_updated_at = models.DateTimeField(auto_now=True)


