from django.contrib import admin
from workorders.models import WorkOrder, Customer, Station, Terminal

class TerminalInline(admin.TabularInline):
  model = Terminal
  extra = 3
  exclude = ('last_edited_by',)

class StationsInline(admin.TabularInline):
  model = Station
  extra = 3
  exclude = ('last_edited_by',)

class CustomerAdmin(admin.ModelAdmin):
  list_display = ('name', 'official_name', 'address', 'last_edited_by')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  inlines = [StationsInline]

class StationAdmin(admin.ModelAdmin):
  list_display = ('number', 'name', 'official_name', 'address', 'customer',
                 'last_edited_by')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  inlines = [TerminalInline]
  list_filter = ['customer']
  search_fields = ['number', 'name']

class TerminalAdmin(admin.ModelAdmin):
  list_display = ('station', 'number', 'crip', 'last_edited_by')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  list_filter = ['crip', 'number']
  search_fields = ['station__name', 'station__number']

class WorkorderAdmin(admin.ModelAdmin):
  list_display = ('customer', 'station', 'terminal', 'device',
                  'pub_date', 'finish_date', 'work_assigned_to',
                  'last_edited_by', 'mod_date')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  list_filter = ['customer', 'device']
  search_fields = ['customer__name', 'station__name']

admin.site.register(WorkOrder, WorkorderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Terminal, TerminalAdmin)
