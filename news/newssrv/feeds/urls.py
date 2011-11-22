from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseNotAllowed

import urllib2
from xml.dom.minidom import parse, parseString

from feeds.models import Source, Article

#import simplejson as json
import json

def get_feed(request, id):
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
            gid = item.getElementsByTagName('guid')[0].firstChild.nodeValue
            date = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue
            description = item.getElementsByTagName('description')[0].firstChild.nodeValue
            #pub_date = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue
            #print '->', title, gid, date

            if not Article.objects.select_related().filter(source=source, gid=gid):
                Article.objects.create(source=source, gid=gid, title=title, description=description)
    else:
        print 'No changes to be done'

    return HttpResponse('This is the home page')

def fetch_feed(request, id):
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

    #return render_to_response('feeds.json', sdict)


urlpatterns = patterns('',
    (r'^(?P<id>[A-Z]{2})', fetch_feed),
)
