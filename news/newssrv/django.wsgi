import os
import socket
import sys

# for debugging
sys.stdout = sys.stderr

if socket.gethostname() == 'dlib-oxgangs.ucs.ed.ac.uk':
    newshome = '/home/ghamilt2/local/news'
else:
    newshome = '/home/gmh04/local/news'

# see http://code.google.com/p/modwsgi/wiki/VirtualEnvironments for potential problems with using activate_this
activate_this = '%s/bin/activate_this.py' % newshome
execfile(activate_this, dict(__file__=activate_this))

if newshome not in sys.path:
    sys.path.append(newshome)

#print sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'newssrv.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
