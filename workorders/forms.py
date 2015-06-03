from django import forms
from django.contrib.auth.models import User
from workorders import models
from smart_selects.form_fields import ChainedModelChoiceField

class UserLoginForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ('username',
              'password')

class WorkOrderForm(forms.ModelForm):
  class Meta:
    model = models.WorkOrder
    fields = ('customer',
              'station',
              'terminal',
              'device',
              'finished',
              'finish_date',
              'work_assigned_to',
              'issue_description',
              'solution_description')
    widgets = {'description': forms.Textarea(attrs={'cols': 40, 'rows': 4}),}

class NewWorkOrderForm(WorkOrderForm):
  finish_date = forms.DateTimeField(widget=forms.HiddenInput(), required=False, label='')
