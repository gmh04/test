from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import newssrv.views


urlpatterns = patterns('',
    # Example:
    (r'^feed/', include('newssrv.feeds.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #(r'^accounts/', include('registration.backends.default.urls')),
    (r'^login$', newssrv.views.login_user),
    (r'^logout$', newssrv.views.logout_user),
    (r'^$', newssrv.views.main),
)

# import settings
# if settings.DEBUG:
    
#     urlpatterns += patterns('',
#                             url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
#                                 {
#                 'document_root': settings.STATIC_ROOT,
#                 }),
#                             )
    
