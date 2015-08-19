from django.contrib import admin
from workorders import models

class TerminalInline(admin.TabularInline):
  model = models.Terminal
  extra = 3
  exclude = ('last_edited_by',)

class StationsInline(admin.TabularInline):
  model = models.Station
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

class DeviceAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_date')
  search_fields = ['name']

class WorkorderAdmin(admin.ModelAdmin):
  list_display = ('customer', 'station', 'terminal', 'device',
                  'pub_date', 'author','start_date','finish_date',
                  'work_assigned_to','last_edited_by', 'mod_date')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  list_filter = ['customer', 'device']
  search_fields = ['customer__name', 'station__name', 'device__name']

admin.site.register(models.WorkOrder, WorkorderAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Station, StationAdmin)
admin.site.register(models.Terminal, TerminalAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.UserProfile)