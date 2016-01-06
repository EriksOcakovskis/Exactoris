from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.validators import URLValidator
from tasks import models
from tasks import forms
from lib.site_globals import get_query
from operator import attrgetter

def user_login(request):
  redirect_to = request.REQUEST.get('next')
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    login_form = forms.UserLoginForm(request.POST)
    user = authenticate(username=username, password=password)

    if login_form.is_valid():
        login(request, user)
        if redirect_to != 'None':
          return HttpResponseRedirect(redirect_to)
        else:
          return HttpResponseRedirect(reverse('tasks:open'))
    else:
      print(login_form.errors)
  else:
    login_form = forms.UserLoginForm()

  context = {'title': 'Login',
             'form':login_form,
             'next':redirect_to}

  return render(request, 'tasks/login.html', context)

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('tasks:login'))

@login_required
def open(request):
  if ('q' in request.GET) and request.GET['q'].strip():
    open_task_list = models.Task.objects.\
                   exclude_by_status_assigned_to(request.user.username, 'Done')
  else:
    open_task_list = models.Task.objects.exclude_by_status('Done').\
                     order_by('registered')

  context = {'title': 'Open',
             'time_now': timezone.now(),
             'open_task_list': open_task_list}

  return render(request, 'tasks/open.html', context)

@login_required
def all(request):
  query_string = ''
  found_entries = None

  if ('q' in request.GET) and request.GET['q'].strip():
    query_string = request.GET['q']

    entry_query = get_query(query_string, \
      ['summary', 'id', 'assigned_to__user__username',])

    all_task_list = models.Task.objects.order_by('registered')\
                    .filter(entry_query)
  else:
    all_task_list = models.Task.objects.order_by('registered')

  context = {'title': 'All',
             'task_list': all_task_list}

  return render(request, 'tasks/all.html', context)

def autodate_on_finished(form_data):
  updated_form = form_data.save(commit=False)
  updated_form.finish_date = timezone.now()

def add_author(form_data, request):
  updated_form = form_data.save(commit=False)
  updated_form.author = request.user

def add_last_edited_by(form_data, request):
  updated_form = form_data.save(commit=False)
  updated_form.last_edited_by = request.user.username

@login_required
def add(request):
  if request.method == 'POST':
    add_form = forms.NewTaskForm(request.POST)
    # if request.POST.get('finished') == 'on':
    #   add_form.fields['solution_description'].required = True
    #   add_form.fields['finish_date'].required = True
    if add_form.is_valid():
      if add_form.cleaned_data['finished'] == True and not add_form.cleaned_data['finish_date']:
        add_author(add_form, request)
        add_last_edited_by(add_form, request)
        autodate_on_finished(add_form)
        add_form.save()
      else:
        add_author(add_form, request)
        add_last_edited_by(add_form, request)
        add_form.save()
      return HttpResponseRedirect(reverse('tasks:open'))
    else:
      print(add_form.errors)
  else:
    add_form = forms.NewTaskForm()#initial={'call_date' : timezone.now()})

  context = {'form': add_form,
             'title': 'Add'}

  return render(request, 'tasks/add.html', context)

@login_required
def detail(request, task_id):
  task = get_object_or_404(models.Task, pk=task_id)

  next_tks = models.Task.objects.filter(id__gt=task.id).order_by('id')[0:1]
  previous_tsk = models.Task.objects.filter(id__lt=task.id).order_by('id')[0:1].reverse()

  if request.method == 'POST':
    detail_form = forms.TaskForm(request.POST, instance = task)
    if request.POST.get('finished') == 'on':
      detail_form.fields['solution_description'].required = True
      detail_form.fields['finish_date'].required = True
    if detail_form.is_valid():
      if detail_form.cleaned_data['finished'] == True and not detail_form.cleaned_data['finish_date']:
        add_last_edited_by(detail_form, request)
        autodate_on_finished(detail_form)
        detail_form.save()
      else:
        add_last_edited_by(detail_form, request)
        detail_form.save()
      return HttpResponseRedirect(reverse('tasks:detail', args=(task.id,)))
    else:
      print(detail_form.errors)
  else:
    detail_form = forms.TaskForm(instance = task)

  context = {'task': task,
             'form': detail_form,
             'next_tks': next_tks,
             'previous_tsk': previous_tsk,
             'title': 'Detail'}
  return render(request, 'tasks/detail.html', context)

@login_required
def reports(request):
  all_task_list = models.task.objects.order_by('-call_date')
  context = {'all_tasks': all_task_list}
  return render(request, 'tasks/reports.html', context)
