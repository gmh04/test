from django.db import models
from django_countries import CountryField

class Source(models.Model):
    country = CountryField()
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=128)

    last_updated = models.DateTimeField(null=True)

class Article(models.Model):
    source = models.ForeignKey(Source)
    title = models.CharField(max_length=32)
    gid = models.CharField(max_length=64)
    description = models.TextField()
    #last_updated = models.DateTimeField()
