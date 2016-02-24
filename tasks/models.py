from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from lib.site_globals import strfdelta
from django.db.models.signals import post_init
import datetime
import calendar

class TaskManager(models.Manager):
  def authored_by(self, author):
    return self.filter(author__username=author)

  def assigned_to(self, user):
    return self.filter(assigned_to__user__username__icontains=user)

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
  # Is the task recurring
  recurring = models.BooleanField('Is the task recurring?', default=False)
  # Foreign key to the type of recurrence (day, month, week, year)
  yearly = 1
  monthly = 2
  weekly = 3
  daily = 4
  RECURRENCE_CHOICES = (
    (yearly, 'Yearly'),
    (monthly, 'Monthly'),
    (weekly, 'Weekly'),
    (daily, 'Daily'),
  )
  typeof_recurrence = models.IntegerField(
    choices=RECURRENCE_CHOICES,
    blank=True,
    null=True
  )
  # Date of recurrence
  dateof_recurrence = models.DateField(blank=True, null=True)
  # Date and time when the task was started
  start_date = models.DateTimeField(blank=True, null=True)
  # Priority of the task
  priority = models.ForeignKey(Priority)
  # Status of the task
  in_progress = 1
  overdue = 2
  on_hold = 3
  done = 4
  to_do = 5
  STATUS_CHOICES = (
    (in_progress, 'In progress'),
    (overdue, 'Overdue'),
    (on_hold, 'On hold'),
    (done, 'Done'),
    (to_do, 'To-Do'),
  )
  status = models.IntegerField(
    choices=STATUS_CHOICES,
    default=to_do
  )
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
      if self.status == done:
        delta = self.complete_date - start
      else:
        delta = current_datetime - start
      result = strfdelta(delta, "{D}d {H:02}h {M:02}m {S:02}s")
    return result
  # How long the task has been worked on
  work_time = property(_get_work_time)
  objects = TaskManager()

  def check_overdue(self):
    if self.status != self.done and self.deadline:
      if str(self.deadline) < str(timezone.now())[:10]:
        self.status = self.overdue
    if self.status == self.overdue:
      if str(self.deadline) >= str(timezone.now())[:10]:
        self.status = self.to_do

  def add_months(self, source_date, months):
    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12 )
    month = month % 12 + 1
    day = min(source_date.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

  def add_days(self, source_date, days):
    month = source_date.month
    year = source_date.year
    day = source_date.day
    max_day = calendar.monthrange(year,month)[1]
    if (int(day) + days) > int(max_day):
      day = (int(day) + days) - max_day
      month = month % 12 + 1
      if month == 1:
        year = int(source_date.year + 1 )
    else:
      day += days
    return datetime.date(year,month,day)

  def recurrence_check(self, dt):
    if self.typeof_recurrence == 1: # yearly
      newdate = self.add_months(dt, 12)
      self.deadline = newdate
    if self.typeof_recurrence == 2: # monthly
      newdate = self.add_months(dt, 1)
      self.deadline = newdate
    if self.typeof_recurrence == 3: # weekly
      newdate = self.add_days(dt, 7)
      self.deadline = newdate
    if self.typeof_recurrence == 4: # daily
      newdate = self.add_days(dt, 1)
      self.deadline = newdate

  def append_to_work_log(self):
    wl = WorkLog.objects.create(
      task=Task.objects.get(id=self.id),
      start_date=self.start_date,
      complete_date=self.complete_date,
      assigned_to=str(self.assigned_to),
      notes=self.commentary
    )
    wl.save()

  def recurrence_pre_save(self):
    if self.recurring == True:
      if self.deadline == None:
        datetime_now = timezone.now()
        self.recurrence_check(datetime_now)
      else:
        if self.status == self.done:
          self.append_to_work_log()
          self.status = self.to_do
          deadline_post = self.deadline
          self.recurrence_check(deadline_post)
          self.start_date = None
          self.complete_date = None

  def save(self, *args, **kwargs):
    self.recurrence_pre_save()
    if not self.id:
      self.registered = timezone.now()
    self.last_edited = timezone.now()
    return super(Task, self).save(*args, **kwargs)

  def __str__(self):
    return '%s - %s' % (str(self.id), self.summary )

class WorkLog(models.Model):
  task = models.ForeignKey(Task)
  start_date = models.DateTimeField(blank=True, null=True)
  complete_date = models.DateTimeField(blank=True, null=True)
  assigned_to = models.CharField(max_length=50, blank=True, null=True)
  notes = models.TextField(blank=True, null=True)

  def __str__(self):
    return '{0} {1} {2} {3}'.format(
      self.start_date,
      self.complete_date,
      self.assigned_to,
      self.notes
    )

def task_post_init(sender, instance, **kwargs):
  if instance.pk:
    instance.check_overdue()

post_init.connect(
  task_post_init,
  sender=Task,
  dispatch_uid='task.signals.task_post_init',)
