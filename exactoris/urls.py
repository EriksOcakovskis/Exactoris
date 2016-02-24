from django.conf.urls import patterns, include, url
from django.contrib import admin
import tasks.views

urlpatterns = [
  url(r'^$', tasks.views.open, name='home'),
  url(r'^tasks/', include('tasks.urls', namespace='tasks')),
  url(r'^admin/', include(admin.site.urls)),
]
