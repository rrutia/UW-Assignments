import os
import sys
path1 = '/home/python/week7'
path2 = '/home/python/week7/blog'
sys.path.insert(0, path1)
sys.path.insert(1, path2)
os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
