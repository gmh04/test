from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render_to_response


import urllib2
from xml.dom.minidom import parse, parseString

from feeds.models import Source, Article

#import simplejson as json
import json


def fetch_feeds_by_source(request, id):
    #get_feed(request, id)

    sdict = {}
    sources = Source.objects.filter(country="UK")

    for source in sources:
        #articles = Article.objects.select_related().filter(source=source).order_by('pub_date')[:5]
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
    articles = Article.objects.filter(source__country=id)[:20]
    return render_to_response('articles.html', {'articles': articles})

urlpatterns = patterns('',
    (r'^(?P<id>[A-Z]{2})', fetch_articles),
)
