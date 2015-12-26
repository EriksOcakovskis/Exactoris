# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext as _
# from django.contrib.auth import authenticate
# from tasks import models
# from smart_selects.form_fields import ChainedModelChoiceField

# class UserLoginForm(forms.ModelForm):
#   password = forms.CharField(widget=forms.PasswordInput())

#   class Meta:
#     model = User
#     fields = ('username',
#               'password')

#   def clean(self):
#     username = self.cleaned_data.get('username')
#     password = self.cleaned_data.get('password')
#     user = authenticate(username=username, password=password)
#     if not user:
#       raise forms.ValidationError(
#         _('The username and password were incorrect.'),
#         code='Wrong login')
#     elif not user.is_active:
#       raise forms.ValidationError(
#         _('The login is valid, but the account has been disabled.'),
#         code='Locked user')

# class TaskForm(forms.ModelForm):
#   class Meta:
#     model = models.task
#     fields = ('customer',
#               'station',
#               'terminal',
#               'device',
#               'call_date',
#               'start_date',
#               'finished',
#               'finish_date',
#               'work_assigned_to',
#               'err_symp_id',
#               'issue_description',
#               'err_cause_id',
#               'perf_act_id',
#               'solution_description',
#               'rnd_used',
#               'field_eng_used',)
#     widgets = {'issue_description': forms.Textarea(attrs={'cols': 50, 'rows': 4}),
#                'solution_description': forms.Textarea(attrs={'cols': 50, 'rows': 4}),
#                'finish_date': forms.DateInput(format='%Y-%m-%d %H:%M:%S'),
#                'start_date': forms.DateInput(format='%Y-%m-%d %H:%M:%S'),
#                'call_date': forms.DateInput(format='%Y-%m-%d %H:%M:%S'),}

#   def clean(self):
#     cleaned_data = super(TaskForm, self).clean()
#     start_date = cleaned_data.get('start_date')
#     finish_date = cleaned_data.get('finish_date')

#     if start_date and finish_date:
#       if finish_date <= start_date:
#         self.add_error('finish_date', ValidationError(
#                       _('Work "finish date" cant be before or at "start date"'),
#                       code='Wrong date/time',))

# class NewTaskForm(TaskForm):
#   finish_date = forms.DateTimeField(required=False)
