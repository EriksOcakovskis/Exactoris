from django.conf.urls import patterns, url
from workorders import views

urlpatterns = patterns('',
  # ex: /workorders/
  url(r'^$', views.open, name='open'),
  # ex: /workorders/login/
  url(r'^login/$', views.user_login, name='login'),
  # ex: /workorders/logout/
  url(r'^logout/$', views.user_logout, name='logout'),
  # ex: /workorders/open/
  url(r'^open/', views.open, name='open'),
  # ex: /workorders/all/
  url(r'^all/', views.all, name='all'),
  # ex: /workorders/add/
  url(r'^add/', views.add, name='add'),
  # ex: /workorders/123/
  url(r'^(?P<workorder_id>\d+)/$', views.detail, name='detail'),
  # ex: /workorders/123/edit/
  url(r'^(?P<workorder_id>\d+)/edit/$', views.detail, name='edit'),
)
