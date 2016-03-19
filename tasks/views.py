from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.validators import URLValidator
from django.db.models import Q
from tasks import models
from tasks import forms
from lib.site_globals import get_query
from operator import attrgetter
import datetime

def user_login(request):
  redirect_to = request.GET.get('next')
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
    open_task_list = models.Task.objects\
      .assigned_to(request.user.username)\
      .exclude(status=4)\
      .order_by('registered')
  else:
    open_task_list = models.Task.objects\
      .exclude(status=4)\
      .order_by('registered')

  context = {'title': 'Open',
             'open_task_list': open_task_list}

  return render(request, 'tasks/open.html', context)

@login_required
def all(request):
  query_string = ''
  found_entries = None

  if ('q' in request.GET) and request.GET['q'].strip():
    query_string = request.GET['q']

    entry_query = get_query(
      query_string,
      [
        'summary',
        'id',
        'category__name',
        'assigned_to__user__username',
        'deadline',
        'complete_date'
      ]
    )

    status_reverse = dict((v, k) for k, v in models.Task.STATUS_CHOICES)
    try:
      status_query=Q(status=status_reverse[query_string.title()])
      all_task_list = models.Task.objects.order_by('registered')\
                    .filter(status_query | entry_query)
    except KeyError:
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
  if request.user.first_name or request.user.last_name:
    updated_form.last_edited_by = \
      request.user.first_name + ' ' + request.user.last_name
  else:
    updated_form.last_edited_by = request.user.username

def get_status_id(status_name):
  s = models.Status.objects.get(name=status_name)
  return s.id

def get_status_name(status_id):
  s = models.Status.objects.get(id=status_id)
  return s.name

def set_req_fields(status_id, form):
  if status_id == '4': # status 'Done'
    form.fields['start_date'].required = True
    form.fields['complete_date'].required = True
    form.fields['assigned_to'].required = True
  if status_id == '1': # status 'In progress'
    form.fields['start_date'].required = True
    form.fields['assigned_to'].required = True

# def overdue_check(status_id, deadline, form):
#   if status_id == '2': # status 'Overdue'
#     deadline_iso = datetime.datetime.strptime(deadline, '%d.%m.%Y')\
#       .date().isoformat()
#     if deadline_iso >= str(timezone.now())[:10]:
#       form.add_error('status', ValidationError(
#                       _('Status is "Overdue" but "Deadline" is in the future!'),
#                       code='Wrong status',))
#       form.add_error('deadline', ValidationError(
#                       _('Are you sure about the "Deadline"?'),
#                       code='Wrong deadline',))

@login_required
def add(request):
  if request.method == 'POST':
    add_form = forms.NewTaskForm(request.POST)
    post_recurring = request.POST.get('recurring')
    post_deadline = request.POST.get('deadline')
    post_status = request.POST.get('status')
    set_req_fields(post_status, add_form)
    # overdue_check(post_status, post_deadline, add_form)
    if add_form.is_valid():
      add_author(add_form, request)
      add_last_edited_by(add_form, request)
      add_form.save()
      return HttpResponseRedirect(reverse('tasks:open'))
    else:
      print(add_form.errors)
  else:
    add_form = forms.NewTaskForm()

  context = {'form': add_form,
             'title': 'Add'}

  return render(request, 'tasks/add.html', context)

@login_required
def detail(request, task_id):
  task = get_object_or_404(models.Task, pk=task_id)

  work_log = models.WorkLog.objects.filter(task=task_id)\
    .order_by('complete_date')

  next_tks = models.Task.objects.filter(id__gt=task.id).order_by('id')[0:1]
  previous_tsk = models.Task.objects.filter(id__lt=task.id)\
                 .order_by('id')[0:1].reverse()

  if request.method == 'POST':
    detail_form = forms.TaskForm(request.POST, instance = task)
    post_recurring = request.POST.get('recurring')
    post_status = request.POST.get('status')
    post_deadline = request.POST.get('deadline')
    set_req_fields(post_status, detail_form)
    # overdue_check(post_status, post_deadline, detail_form)
    if detail_form.is_valid():
      add_last_edited_by(detail_form, request)
      detail_form.save()
      return HttpResponseRedirect(reverse('tasks:detail', args=(task.id,)))
    else:
      print(detail_form.errors)
  else:
    detail_form = forms.TaskForm(instance = task)

  context = {'task': task,
             'work_log':work_log,
             'form': detail_form,
             'next_tks': next_tks,
             'previous_tsk': previous_tsk,
             'title': 'Detail'}
  return render(request, 'tasks/detail.html', context)

@login_required
def reports(request):
  all_task_list = models.Task.objects.order_by('-registered')
  context = {'all_tasks': all_task_list}
  return render(request, 'tasks/reports.html', context)
