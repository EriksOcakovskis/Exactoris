from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from lib.site_globals import strfdelta

class WorkOrderManager(models.Manager):
  def authored_by(self, author):
    return self.filter(author__username=author)

  def assigned_to(self, user):
    return self.filter(work_assigned_to__user__username__icontains=user)

class UserProfile(models.Model):
  user = models.OneToOneField(User)

  def __str__(self):
    return self.user.username

class Customer(models.Model):
  name = models.CharField(max_length=50)
  official_name = models.CharField(max_length=80)
  address = models.CharField(max_length=80)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return self.name

class Station(models.Model):
  name = models.CharField(max_length=50)
  number = models.CharField(max_length=4)
  official_name = models.CharField(max_length=80)
  address = models.CharField(max_length=80)
  customer = models.ForeignKey(Customer)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return '%s - %s' % (self.name, self.number)

class Terminal(models.Model):
  number = models.CharField(max_length=2)
  crip = models.BooleanField('Is this a CRIP?', default=False)
  station = models.ForeignKey(Station)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return self.number

class Device(models.Model):
  name = models.CharField(max_length=50)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)

  def __str__(self):
    return self.name

class ErrorSymptom(models.Model):
  code = models.CharField(max_length=4)
  description = models.CharField(max_length=80)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)

  def __str__(self):
    return '%s %s' % (self.code, self.description)

class ErrorCause(models.Model):
  code = models.CharField(max_length=4)
  description = models.CharField(max_length=80)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)

  def __str__(self):
    return '%s %s' % (self.code, self.description)

class PerformedActions(models.Model):
  code = models.CharField(max_length=4)
  description = models.CharField(max_length=80)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)

  def __str__(self):
    return '%s %s' % (self.code, self.description)

class WorkOrder(models.Model):
  customer = models.ForeignKey(Customer)
  station = ChainedForeignKey(
    Station,
    chained_field="customer",
    chained_model_field="customer",
    show_all=False,
    auto_choose=True
  )
  terminal = ChainedForeignKey(
    Terminal,
    chained_field="station",
    chained_model_field="station",
    show_all=False,
    auto_choose=True
  )
  device = models.ForeignKey(Device, blank=True, null=True)
  # Symptom ID, what symptoms were reported, sales down, one product down, so on
  err_symp_id = models.ForeignKey(ErrorSymptom, blank=True, null=True)
  #
  issue_description = models.TextField(blank=False)
  # Error cause ID, breakdown reason generic and specific codes
  err_cause_id = models.ForeignKey(ErrorCause, blank=True, null=True)
  # Preformed action ID, generic action codes
  perf_act_id = models.ForeignKey(PerformedActions, blank=True, null=True)
  #
  solution_description = models.TextField(blank=True)
  # When work order was registered in database
  pub_date = models.DateTimeField(auto_now_add=True, blank=False)
  # When complaint from customer was received
  call_date = models.DateTimeField('Complaint date', blank=False)

  def _one_day_hence(self):
    return self.call_date + timezone.timedelta(days=1)

  # Latest date-time when work should be started on work order
  req_start_date = property(_one_day_hence)
  # When work on workorder was started
  start_date = models.DateTimeField(blank=True, null=True)
  author = models.ForeignKey(User)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  finished = models.BooleanField('Is the job finished?', default=False)
  finish_date = models.DateTimeField('Job complete date', blank=True, null=True)

  def _get_workorder_open_time(self):
    current_datetime = timezone.now()
    saved_datetime = self.call_date
    if self.finished == True:
      delta = self.finish_date - saved_datetime
    else:
      delta = current_datetime - saved_datetime
    result = strfdelta(delta, "{D}d {H:02}h {M:02}m {S:02}s")
    return result

  workorder_open_time = property(_get_workorder_open_time)
  work_assigned_to = models.ForeignKey(UserProfile, blank=True, null=True)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)
  # Was the work forwarded to RND?
  rnd_used = models.BooleanField('Was RND used?', default=False)
  # Was the work forwarded to field engineers?
  field_eng_used = models.BooleanField('Redirected to field engineers?', default=False)
  objects = WorkOrderManager()

  def __str__(self):
    return str(self.id)
