from django.conf.urls.defaults import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import URLValidator
from django_countries.fields import Country
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render_to_response

import json
import urllib2

from urllib2 import URLError, HTTPError
from xml.dom.minidom import parse, parseString

from newssrv.feeds.models import Source, Article


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

    #print sdict
    return HttpResponse(json.dumps(sdict), mimetype='application/json')


def fetch_articles(request, id):
    country = None
    articles = None

    try:
        country = Source.objects.get(country=id).country
        articles = Article.objects.filter(
            source__country=id).order_by('-date')[:20]
    except ObjectDoesNotExist:
        country = Country(code=id)

    return render_to_response('articles.html', {'articles': articles,
                                                'country': country})


def suggest_feed(request, country_id):
    success = False
    message = None

    url = request.GET['url']

    validate = URLValidator(verify_exists=False)
    try:
        print validate(request.GET['url'])
        try:
            urllib2.urlopen(url)

            try:
                Source.objects.get(feed_url=url)
                message = '%s already exists' % url
            except Source.DoesNotExist:
                Source(feed_url=url, country=country_id).save()
                success = True
        except (URLError, HTTPError) as e:
            message = 'Problem reading url: %s' % e

    except ValidationError, e:
        message = 'Invalid URL'

    return render_to_response('suggest_response.html',
                              {'success': success,
                               'message': message})


urlpatterns = patterns('',
    (r'^(?P<id>[A-Z]{2})', fetch_articles),
    (r'^suggest/(?P<country_id>[A-Z]{2}).+$', suggest_feed),
)
