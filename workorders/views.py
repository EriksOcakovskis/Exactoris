from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from workorders import models
from workorders import forms
from lib.site_globals import get_query

def user_login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse('workorders:latest'))
      else:
        return HttpResponse("Your Rango account is disabled.")
    else:
      return HttpResponse("Invalid login details supplied.")
  else:
    user_login_form = forms.UserLoginForm()

    context = {'title': 'Login',
               'form':user_login_form}

    return render(request, 'workorders/login.html', context)

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('workorders:login'))

@login_required
def latest(request):
  latest_workorder_list = models.WorkOrder.objects.order_by('-pub_date')[:5]

  elapsed_list = []
  for wo in latest_workorder_list:
    elapsed_list.append(wo.elapsed_time_delta())

  workorder_elapsed_list = []
  c = 0
  for wo in latest_workorder_list:
    workorder_elapsed_list.append([wo,elapsed_list[c]])
    c = c + 1

  context = {'title': 'Latest',
             'workorder_elapsed_list': workorder_elapsed_list}

  return render(request, 'workorders/latest.html', context)

@login_required
def all(request):
  all_workorder_list = models.WorkOrder.objects.order_by('-pub_date')
  query_string = ''
  found_entries = None

  if ('q' in request.GET) and request.GET['q'].strip():
    query_string = request.GET['q']

    entry_query = get_query(query_string, ['station__name', 'customer__name',])

    found_entries = all_workorder_list.filter(entry_query)

    context = {'title': 'All',
               'workorder_list': found_entries}
  else:
    context = {'title': 'All',
               'workorder_list': all_workorder_list}

  return render(request, 'workorders/all.html', context)

@login_required
def add(request):
  if request.method == 'POST':
    add_form = forms.WorkOrderForm(request.POST)
    if add_form.is_valid():
      add_form.save()
      return HttpResponseRedirect(reverse('workorders:latest'))
    else:
      print(add_form.errors)
  else:
    add_form = forms.WorkOrderForm()

  context = {'form': add_form,
             'title': 'Add'}

  return render(request, 'workorders/add.html', context)

@login_required
def detail(request, workorder_id):
  workorder = get_object_or_404(models.WorkOrder, pk=workorder_id)
  elapsed = workorder.elapsed_time_delta()

  next_wo = models.WorkOrder.objects.filter(id__gt=workorder.id).order_by('id')[0:1]
  previous_wo = models.WorkOrder.objects.filter(id__lt=workorder.id).order_by('id')[0:1].reverse()

  if request.method == 'POST':
    detail_form = forms.WorkOrderForm(request.POST, instance = workorder)
    if detail_form.is_valid():
      detail_form.save()
      return HttpResponseRedirect(reverse('workorders:detail', args=(workorder.id,)))
    else:
      print(detail_form.errors)
  else:
    detail_form = forms.WorkOrderForm(instance = workorder)

  context = {'workorder': workorder,
             'form': detail_form,
             'elapsed': elapsed,
             'next_wo': next_wo,
             'previous_wo': previous_wo,
             'title': 'Detail'}
  return render(request, 'workorders/detail.html', context)

