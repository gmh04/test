from django.conf.urls.defaults import *

from newssrv.feeds.views import fetch_articles, suggest_feed

urlpatterns = patterns('',
    (r'^(?P<id>[A-Z]{2})', fetch_articles),
    (r'^suggest/(?P<country_id>[A-Z]{2}).+$', suggest_feed),
)
