from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
  url(r'^$', 'tasks.views.open', name='home'),
  url(r'^tasks/', include('tasks.urls', namespace='tasks')),
  url(r'^chaining/', include('smart_selects.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
