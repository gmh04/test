from django.conf.urls.defaults import *

from newssrv.feeds.views import *

urlpatterns = patterns('',
    (r'^(?P<id>[A-Z]{2})', fetch_articles),
    (r'^suggest/(?P<country_id>[A-Z]{2}).+$', suggest_feed),
    (r'^edit/[A-Z]{2}/(?P<source_id>\d)$', edit_source),
    (r'^edit/(?P<country_id>[A-Z]{2})$', fetch_sources_by_country),
    (r'^edit/', fetch_all_countries),
    # (r'^edit/(?P<country_id>[A-Z]{2})', fetch_feeds_by_country),
)
