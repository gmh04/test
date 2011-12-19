from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import mail_admins
from django.core.validators import URLValidator
from django_countries.fields import Country
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from urllib2 import URLError, HTTPError
from xml.dom.minidom import parse, parseString

import json
import os
import urllib2

from newssrv.feeds.models import Source, Article
from newssrv import settings

def fetch_all_countries(request):
    countries = []
    sources = Source.objects.values('id', 'country').distinct()

    for source in sources:
        countries.append(Country(code=source['country']))

    return render_to_response('edit_countries.html', {'countries': countries})

def fetch_sources_by_country(request, country_id):
    country = Country(code=country_id)
    sources = Source.objects.filter(country=country_id)
    return render_to_response('edit_country.html',
                              {'country': country,
                               'sources': sources})

def _handle_uploaded_file(f, name):

    destination = open(
        os.sep.join((settings.STATIC_ROOT, 'icons', name)),
        'wb+')

    print os.sep.join((settings.STATIC_ROOT, 'icons', name))

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def edit_source(request, source_id):
    source = Source.objects.get(id=source_id)

    icon = None

    from newssrv.feeds.forms import EditSource

    if request.method == 'POST':
        form = EditSource(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['icon']
            icon_name = '%s.%s' % (source_id, f.name.split('.')[1])

            _handle_uploaded_file(f, icon_name)

            source.feed_url = form.cleaned_data['feed_url']
            source.icon = icon_name
            source.save()
            return redirect('/?country=%s&source=%d' % (source.country, source.id))
        else:
            print form.errors
    else:
        # form = EditSource(instance=source)
        if '/' in source.feed_url:
            source_icon =  source.feed_url
        else:
            source_icon = '/static/icons/%s' % source.feed_url
            
        form = EditSource(initial={'feed_url': source.feed_url})

    return render_to_response('edit_source.html',
                              {'source': source,
                               'form': form},
                              context_instance=RequestContext(request))

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
    source_icon = None

    try:
        #country = Source.objects.get(country=id).country
        country = Country(code=id)
        articles = Article.objects.filter(
            source__country=id).order_by('-date')[:20]
        source_icon = _get_source_icon(articles[0].source)
    except ObjectDoesNotExist:
        #country = Country(code=id)
        pass
    print '***', source_icon
    return render_to_response('articles.html', {'articles': articles,
                                                'country': country,
                                                'source_icon': source_icon})


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
                mail_admins('URL suggested', url)
                success = True
        except (URLError, HTTPError) as e:
            message = 'Problem reading url: %s' % e

    except ValidationError, e:
        message = 'Invalid URL'

    return render_to_response('suggest_response.html',
                              {'success': success,
                               'message': message},
                              context_instance=RequestContext(request))
def _get_source_icon(source):
    if '/' in source.feed_url:
        source_icon = source.icon
    else:
        source_icon = '/static/icons/%s' % source.feed_icon

    return source_icon
