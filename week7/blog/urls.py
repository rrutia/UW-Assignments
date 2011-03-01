from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index', name="homepage_home"),
    url(r'^about/$', 'blog.views.about', name="homepage_about"),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
