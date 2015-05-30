from django import forms
from workorders import models
from smart_selects.form_fields import ChainedModelChoiceField

# class WorkorderDetailForm(forms.Form):
#   customer = forms.ModelChoiceField(queryset = '', initial='', required=True)
#   station = ChainedModelChoiceField(app_name = 'workorders',
#                                     model_name = 'Station',
#                                     chain_field = 'customer',
#                                     model_field = 'customer',
#                                     show_all = False,
#                                     auto_choose = True,
#                                     queryset = '',
#                                     required=True)
#   terminal = ChainedModelChoiceField(app_name = 'workorders',
#                                      model_name = 'Terminal',
#                                      chain_field = 'station',
#                                      model_field = 'station',
#                                      show_all = False,
#                                      auto_choose = True,
#                                      queryset = '',
#                                      required=True)

class WorkOrderForm(forms.ModelForm):
  class Meta:
    model = models.WorkOrder
    fields = ('customer',
              'station',
              'terminal',
              'device',
              'finish_date',
              'work_assigned_to',
              'description')
    exclude = ('finish_date',)
    widgets = {'description': forms.Textarea(attrs={'cols': 40, 'rows': 4}),}