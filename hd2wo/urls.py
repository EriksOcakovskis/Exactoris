from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
  #url(r'^$', 'hd2wo.views.home', name='home'),
  #url(r'^workorders/', include('workorders.urls', namespace='workorders')),

  url(r'^admin/', include(admin.site.urls)),
)
