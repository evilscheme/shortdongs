from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('shortener.views',
    (r'^$', 'index'),
    (r'^shorten/?$', 'shorten'),
    (r'^dump/$', 'dump'),
    (r'(.*)', 'resolve'),
)
