from datetime import datetime
from urllib2 import URLError, HTTPError

from lxml import etree

import dateutil.parser
import email.utils
import pytz
import time
import urllib2

from django.core.management.base import BaseCommand, CommandError

from newssrv.feeds.models import Article, Source


class Command(BaseCommand):
    help = 'Populates articles from current feeds'

    def handle(self, *args, **options):
        sources = Source.objects.all()

        for source in sources:

            try:
                # fetch feed
                page = urllib2.urlopen(source.feed_url)

                last_modified = None
                if 'last-modified' in page.headers:
                    last_modified = self.str2date(
                        page.headers['last-modified'])
                    last_modified = last_modified.astimezone(pytz.utc)
                if not last_modified:
                    last_modified = datetime.utcnow()

                # remove timezone to allow compare
                last_modified = last_modified.replace(tzinfo=None)

                # parse page for XML processing
                tree = etree.parse(page)
                if not source.last_updated or \
                       source.last_updated < last_modified:
                    self.update_source(tree, source)

                    items = tree.xpath('/rss/channel/item')
                    for item in items:
                        self.update_article(item, source)

                else:
                    print 'No changes to be done'

            except (URLError, HTTPError) as e:
                print e

    def str2date(self, str):
        dt = dateutil.parser.parse(str)

        # convert to UTC, django will store
        return  dt.astimezone(pytz.utc)

    def update_source(self, tree, source):
        # update source incase it has changed
        lastBuildDate = tree.xpath('/rss/channel/lastBuildDate')
        if len(lastBuildDate):
            source.last_updated = self.str2date(lastBuildDate[0].text)
        else:
             source.last_updated = datetime.utcnow()

        source.name = tree.xpath('/rss/channel/title')[0].text
        source.site_url = tree.xpath('/rss/channel/link')[0].text

        language = tree.xpath('/rss/channel/language')
        if len(language):
            source.language = language[0].text

        icon = tree.xpath('/rss/channel/image/url')
        if len(icon):
            source.icon = icon[0].text

        #print source.icon, len(source.icon)

        source.save()

    def update_article(self, item, source):
        url = item.find('link').text
        gid = item.find('guid')

        if gid is not None:
            gid = gid.text
        else:
            # use url if no gid
            gid = url

        if not Article.objects.select_related().filter(source=source, gid=gid):

            title = item.find('title').text
            description = item.find('description').text

            datestr = item.find('pubDate').text
            pub_date = self.str2date(datestr)

            from django.utils.encoding import smart_str, smart_unicode
            #print 'add %s: %s' % (title, gid)
            print smart_str('add %s: %s' % (title, gid))

            Article.objects.create(source=source,
                                   gid=gid,
                                   title=title,
                                   description=description,
                                   date=pub_date,
                                   url=url)
