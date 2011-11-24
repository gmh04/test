from django.db import models
from django_countries import CountryField

class Source(models.Model):
    country = CountryField()
    name = models.CharField(max_length=32)
    feed_url = models.CharField(max_length=128)
    site_url = models.CharField(max_length=128)
    last_updated = models.DateTimeField(null=True)
    language = models.CharField(max_length=5)

class Article(models.Model):
    source = models.ForeignKey(Source)
    title = models.CharField(max_length=32)
    gid = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateTimeField()
    url = models.CharField(max_length=128)
