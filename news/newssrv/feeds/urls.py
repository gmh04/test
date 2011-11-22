from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseNotAllowed

import urllib2
from xml.dom.minidom import parse, parseString

from feeds.models import Source, Article

def fetch_feed(request, id):
    feed = 'http://feeds.bbci.co.uk/news/uk/rss.xml'

    print id

    try:
        page = urllib2.urlopen(feed)
    except Exception as e:
        print e

    last_update = page.headers['last-modified']
    print last_update

    dom = parse(page)
    last_update = dom.getElementsByTagName('lastBuildDate')[0]
    #print dir(last_update)
    #print last_update.firstChild.nodeValue

    source = Source.objects.get(country="UK", name="BBC")

    print source.last_updated

    if source.last_updated < last_update:
        print 'update feeds'

        items = dom.getElementsByTagName('item')
        #print items
        for item in items:
            title = item.getElementsByTagName('title')[0].firstChild.nodeValue
            id = item.getElementsByTagName('guid')[0].firstChild.nodeValue
            date = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue
            description = item.getElementsByTagName('description')[0].firstChild.nodeValue

            if not Article.objects.filter(source=source, id=id):
                Article(id=id, title=title, description=description).save()
    else:
        print 'No changes to be done'

    return HttpResponse('This is the home page')

urlpatterns = patterns('',
    (r'^(?P<id>[A-Z]{2})', fetch_feed),
)
