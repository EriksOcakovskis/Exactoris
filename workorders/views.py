from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from workorders import models
from workorders import forms
from lib.site_globals import get_query

def user_login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    login_form = forms.UserLoginForm(request.POST)
    user = authenticate(username=username, password=password)

    if login_form.is_valid():
        login(request, user)
        return HttpResponseRedirect(reverse('workorders:open'))
    else:
      print(login_form.errors)
  else:
    login_form = forms.UserLoginForm()

  context = {'title': 'Login',
             'form':login_form}

  return render(request, 'workorders/login.html', context)

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('workorders:login'))

@login_required
def open(request):
  open_workorder_list = models.WorkOrder.objects.filter(finished__exact=False) \
    .order_by('call_date')

  if ('q' in request.GET and request.GET['q'].strip()):
    assigned_entries = models.WorkOrder.objects \
      .assigned_to(request.user.username).filter(finished__exact=False) \
      .order_by('call_date')

    context = {'title': 'Open',
               'time_now': timezone.now(),
               'open_workorder_list': assigned_entries}
  else:
    context = {'title': 'Open',
               'time_now': timezone.now(),
               'open_workorder_list': open_workorder_list}

  return render(request, 'workorders/open.html', context)

@login_required
def all(request):
  all_workorder_list = models.WorkOrder.objects.order_by('-call_date')
  query_string = ''
  found_entries = None

  if ('q' in request.GET) and request.GET['q'].strip():
    query_string = request.GET['q']

    entry_query = get_query(query_string, \
      ['station__name', 'customer__name', 'work_assigned_to__user__username',])

    found_entries = all_workorder_list.filter(entry_query)

    context = {'title': 'All',
               'workorder_list': found_entries}
  else:
    context = {'title': 'All',
               'workorder_list': all_workorder_list}

  return render(request, 'workorders/all.html', context)

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
    add_form = forms.NewWorkOrderForm(request.POST)
    if request.POST.get('finished') == 'on':
      add_form.fields['solution_description'].required = True
      add_form.fields['finish_date'].required = True
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
      return HttpResponseRedirect(reverse('workorders:open'))
    else:
      print(add_form.errors)
  else:
    add_form = forms.NewWorkOrderForm(initial={'call_date' : timezone.now()})

  context = {'form': add_form,
             'title': 'Add'}

  return render(request, 'workorders/add.html', context)

@login_required
def detail(request, workorder_id):
  workorder = get_object_or_404(models.WorkOrder, pk=workorder_id)

  next_wo = models.WorkOrder.objects.filter(id__gt=workorder.id).order_by('id')[0:1]
  previous_wo = models.WorkOrder.objects.filter(id__lt=workorder.id).order_by('id')[0:1].reverse()

  if request.method == 'POST':
    detail_form = forms.WorkOrderForm(request.POST, instance = workorder)
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
      return HttpResponseRedirect(reverse('workorders:detail', args=(workorder.id,)))
    else:
      print(detail_form.errors)
  else:
    detail_form = forms.WorkOrderForm(instance = workorder)

  context = {'workorder': workorder,
             'form': detail_form,
             'next_wo': next_wo,
             'previous_wo': previous_wo,
             'title': 'Detail'}
  return render(request, 'workorders/detail.html', context)

