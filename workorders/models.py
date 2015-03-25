from django.db import models

class WorkOrder(models.Model):
  customer = models.CharField(max_length=50)
  station = models.CharField(max_length=50)
  station_number = models.CharField(max_length=4)
  terminal = models.CharField(max_length=2)
  device = models.CharField(max_length=100)
  description = models.TextField(blank=False)
  pub_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  time_elapsed = models.CharField(max_length=20)
  finish_date = models.DateTimeField('Job complete date')
  work_assigned_to = models.CharField(max_length=50, blank=False, null=True)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return self.station_number

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
  official_name = models.CharField(max_length=80)
  address = models.CharField(max_length=80)
  customer = models.ForeignKey(Customer)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return self.name

class Terminal(models.Model):
  number = models.CharField(max_length=2)
  crip = models.CharField(max_length=3)
  station = models.ForeignKey(Station)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return self.number