from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from lib.site_globals import strfdelta

class TaskManager(models.Manager):
  def authored_by(self, author):
    return self.filter(author__username=author)

  def assigned_to(self, user):
    return self.filter(assigned_to__user__username__icontains=user)

  def exclude_by_status(self, status):
    return self.exclude(status__name__exact=status)

  def exclude_by_status_assigned_to(self, user, status):
    t = self.filter(assigned_to__user__username__icontains=user)
    return t.exclude(status__name__exact=status)

class UserProfile(models.Model):
  user = models.OneToOneField(User)

  def __str__(self):
    return '%s %s' % (self.user.first_name, self.user.last_name)

class Priority(models.Model):
  name = models.CharField(max_length=50)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return self.name

class Status(models.Model):
  name = models.CharField(max_length=50)
  created_date = models.DateTimeField(auto_now_add=True, blank=False)
  mod_date = models.DateTimeField(auto_now=True, blank=False)
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)

  def __str__(self):
    return self.name

class Task(models.Model):
  # Task summary, never empty
  summary = models.CharField(blank=False, max_length=80)
  # Task description, can be empty
  description = models.TextField(blank=True, null=True)
  # Date and time when task was created, automatic on submit
  registered = models.DateTimeField(editable=False)
  # Person who created the task, can be website admin
  author = models.ForeignKey(User)
  # To whom this task is assigned to, can't be website admin
  assigned_to = models.ForeignKey(UserProfile, blank=True, null=True)
  # Date and time when the task was started
  start_date = models.DateTimeField(blank=True, null=True)
  # Priority of the task
  priority = models.ForeignKey(Priority)
  # Status of the task
  status = models.ForeignKey(Status)
  # Date and time when the task was complete
  complete_date = models.DateTimeField(blank=True, null=True)
  # When the task needs to be completed
  deadline = models.DateField(blank=True, null=True)
  # A prerequisite task, can be empty
  prerequisite = models.ForeignKey('self', blank=True, null=True)
  # If a prerequisite is not a task use this field to describe it
  prerequisite_description = models.TextField(blank=True, null=True)
  # Date and time when last edit to the task was made
  last_edited = models.DateTimeField()
  # Who last edited the task
  last_edited_by = models.CharField(max_length=50, blank=False, null=True)
  # Additional comments
  commentary = models.TextField(blank=True, null=True)

  def _get_work_time(self):
    current_datetime = timezone.now()
    if self.start_date == null:
      result = "Work is not started yet"
    else:
      start = self.start_date
      if self.status == "Done":
        delta = self.complete_date - start
      else:
        delta = current_datetime - start
      result = strfdelta(delta, "{D}d {H:02}h {M:02}m {S:02}s")
    return result
  # How long the task has been worked on
  work_time = property(_get_work_time)
  objects = TaskManager()

  def save(self, *args, **kwargs):
    if not self.id:
      self.registered = timezone.now()
    self.last_edited = timezone.now()
    return super(Task, self).save(*args, **kwargs)

  def __str__(self):
    return '%s - %s' % (str(self.id), self.summary )
