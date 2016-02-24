from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from tasks import models

class UserLoginForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ('username',
              'password')

  def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
      raise forms.ValidationError(
        _('The username and password were incorrect.'),
        code='Wrong login')
    elif not user.is_active:
      raise forms.ValidationError(
        _('The login is valid, but the account has been disabled.'),
        code='Locked user')

class TaskForm(forms.ModelForm):
  start_date = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S', '%Y-%m-%d %H:%M'],\
    widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M:%S'), required=False)
  complete_date = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S', '%Y-%m-%d %H:%M'],\
    widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M:%S'), required=False)
  deadline = forms.DateField(input_formats=['%d.%m.%Y', '%Y-%m-%d'],\
    widget=forms.DateInput(format='%d.%m.%Y'), required=False)
  dateof_recurrence = forms.DateField(input_formats=['%d.%m.%Y', '%Y-%m-%d'],\
    widget=forms.DateInput(format='%d.%m.%Y'), required=False)
  class Meta:
    model = models.Task
    fields = ('id',
              'summary',
              'priority',
              'status',
              'assigned_to',
              'recurring',
              'typeof_recurrence',
              'dateof_recurrence',
              'deadline',
              'start_date',
              'complete_date',
              'description',
              'prerequisite',
              'prerequisite_description',
              'registered',
              'author',
              'last_edited',
              'last_edited_by',
              'commentary',)
    exclude = ('registered', 'last_edited_by', 'author', 'last_edited',)
    widgets = {'description': forms.Textarea(attrs={'cols': 50, 'rows': 4}),
               'prerequisite_description': forms.Textarea(attrs={'cols': 50, 'rows': 4}),
               'commentary': forms.Textarea(attrs={'cols': 50, 'rows': 4}),}

  def clean(self):
    cleaned_data = super(TaskForm, self).clean()
    start_date = cleaned_data.get('start_date')
    complete_date = cleaned_data.get('complete_date')

    if start_date and complete_date:
      if complete_date <= start_date:
        self.add_error('complete_date', ValidationError(
                    _('Work "complete date" cant be before or at "start date"'),
                    code='Wrong date/time',))

class NewTaskForm(TaskForm):
  complete_date = forms.DateTimeField(required=False)
  class Meta(TaskForm.Meta):
    exclude = ('registered', 'last_edited_by', 'author', 'last_edited',)
