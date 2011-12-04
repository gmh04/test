from django.core.management.base import BaseCommand

from newssrv.feeds.models import Source

import json
import os
import settings

class Command(BaseCommand):
    help = 'Creates an initial_data.json file from current sources'

    def handle(self, *args, **options):
        output = []
        sources = Source.objects.all()

        f = open(os.sep.join((settings.PROJECT_ROOT, 'initial_data.json')), 'w')
 
        for source in sources:
            output.append({
                'model': "feeds.Source",
                'pk': source.id,
                'fields': {
                        'country': source.country.code,
                        'feed_url': source.feed_url
                        }
                })

        f.write(json.dumps(output))
