from django.db import models
from django_countries import CountryField

class Source(models.Model):
    country = CountryField()
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(null=True)

class Article(models.Model):
    #source = models.ForeignKey(Source)
    pass
