from django.conf.urls.defaults import *
from django.core.exceptions import ObjectDoesNotExist
from django_countries.fields import Country
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render_to_response

import urllib2

from xml.dom.minidom import parse, parseString

from feeds.models import Source, Article

import json


def fetch_feeds_by_source(request, id):
    sdict = {}
    sources = Source.objects.filter(country="UK")

    for source in sources:
        articles = Article.objects.select_related().filter(source=source)[:5]
        sdict[source.name] = {}

        for a in articles:
            print dir(a)
            sdict[source.name][a.gid] = {
                'title': a.title,
                'desciption': a.description}

    print sdict
    return HttpResponse(json.dumps(sdict), mimetype='application/json')


def fetch_articles(request, id):
    country = None
    articles = None

    try:
        country = Source.objects.get(country=id).country.name
        articles = Article.objects.filter(
            source__country=id).order_by('-date')[:20]
    except ObjectDoesNotExist:
        country = Country(code=id).name

    return render_to_response('articles.html', {'articles': articles,
                                                'country': country})

urlpatterns = patterns('',
    (r'^(?P<id>[A-Z]{2})', fetch_articles),
)
