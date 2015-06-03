from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

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
  device = models.ForeignKey(Device)
  issue_description = models.TextField(blank=False)
  solution_description = models.TextField(blank=True)
  pub_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  finished = models.BooleanField('Is the job finished?', default=False)
  finish_date = models.DateTimeField('Job complete date', blank=True, null=True)
  work_assigned_to = models.ForeignKey(UserProfile)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def elapsed_time_delta(self):
    current_datetime = timezone.now()
    saved_datetime = self.pub_date
    result = current_datetime - saved_datetime
    return result

  def __str__(self):
    return str(self.id)