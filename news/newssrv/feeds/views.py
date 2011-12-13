from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import mail_admins
from django.core.validators import URLValidator
from django_countries.fields import Country
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

import json
import urllib2

from urllib2 import URLError, HTTPError
from xml.dom.minidom import parse, parseString

from newssrv.feeds.models import Source, Article

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

def edit_source(request, source_id):
    source = Source.objects.get(id=source_id)

    icon = None
    # file_name = '%s-%s' % (source.id, source.icon)
    # if(os.path.exists(os.sep.join((settings.PROJECT_PATH, 'static', 'icons', file_name)))):
    #     icon = '/static/icons/%s' % file_name

    from newssrv.feeds.forms import EditSource

    print request.POST
    print request.FILES
    if request.method == 'POST':
        form = EditSource(request.POST, request.FILES)
        if form.is_valid():
            #form = form.save()
            #print form.feed_url
            #print form
            form.feed_url = form.cleaned_data['feed_url']
            return redirect('/?source=%d' % source.id)
        else:
            print form.errors
    else:
        # form = EditSource(instance=source)        
        form = EditSource(initial={'feed_url': source.feed_url})

    return render_to_response('edit_source.html',
                              {'source': source,
                               'form': form},
                              context_instance=RequestContext(request))
    # return render_to_response('edit_source.html',
    #                           {'source': source,
    #                            'form': form})

    # return render_to_response('edit_source.html',
    #                           {'source': source,
    #                            'icon': icon})

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
        #country = Source.objects.get(country=id).country
        country = Country(code=id)
        articles = Article.objects.filter(
            source__country=id).order_by('-date')[:20]
    except ObjectDoesNotExist:
        #country = Country(code=id)
        pass

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
                mail_admins('URL suggested', url)
                success = True
        except (URLError, HTTPError) as e:
            message = 'Problem reading url: %s' % e

    except ValidationError, e:
        message = 'Invalid URL'

    return render_to_response('suggest_response.html',
                              {'success': success,
                               'message': message})

