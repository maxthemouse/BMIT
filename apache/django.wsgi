import os
import sys

path = '/webroot/bmit'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bmit.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
