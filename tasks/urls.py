from django.conf.urls import patterns, url
from tasks import views

urlpatterns = [
  # ex: /tasks/
  url(r'^$', views.open, name='open'),
  # ex: /tasks/login/
  url(r'^login/$', views.user_login, name='login'),
  # ex: /tasks/logout/
  url(r'^logout/$', views.user_logout, name='logout'),
  # ex: /tasks/open/
  url(r'^open/', views.open, name='open'),
  # ex: /tasks/all/
  url(r'^all/', views.all, name='all'),
  # ex: /tasks/add/
  url(r'^add/', views.add, name='add'),
  # ex: /tasks/reports/
  url(r'^reports/', views.reports, name='reports'),
  # ex: /tasks/123/
  url(r'^(?P<task_id>\d+)/$', views.detail, name='detail'),
  # ex: /tasks/123/edit/
  url(r'^(?P<task_id>\d+)/edit/$', views.detail, name='edit'),
]
