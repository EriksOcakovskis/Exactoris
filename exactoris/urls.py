from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
  url(r'^$', 'workorders.views.open', name='home'),
  url(r'^workorders/', include('workorders.urls', namespace='workorders')),
  url(r'^chaining/', include('smart_selects.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
