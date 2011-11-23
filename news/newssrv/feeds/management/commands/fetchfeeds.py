from urllib2 import URLError, HTTPError
from xml.dom.minidom import parse

import urllib2

from django.core.management.base import BaseCommand, CommandError

from newssrv.feeds.models import Article, Source


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        sources = Source.objects.all()

        for source in sources:
            print source.name, source.url

            try:
                page = urllib2.urlopen(source.url)
                last_update = page.headers['last-modified']
                print last_update

                dom = parse(page)
                last_update = dom.getElementsByTagName('lastBuildDate')[0]

                print source.last_updated

                if source.last_updated < last_update:
                    print 'update feeds'

                    items = dom.getElementsByTagName('item')
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

            except (URLError, HTTPError) as e:
                print e
