from django.db import models


class Scraper(models.Model):

    currency = models.CharField(max_length=50, unique=True)
    value = models.FloatField(default=0)
    frequency = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    value_updated_at = models.DateTimeField(auto_now=True)

    def toDict(self):
        return {
            "id" : self.id,
            "currency" : self.currency,
            "value" : self.value,
            "frequency" : self.frequency,
            "created_at" : self.created_at,
            "value_updated_at" : self.value_updated_at,
        }

