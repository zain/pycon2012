from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crime$', 'django.views.generic.simple.direct_to_template', {'template': 'crime.html'}),
    url(r'^crime.json$', 'maps.crime.views.crime_list'),
)
