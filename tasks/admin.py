from django.contrib import admin
from tasks import models

class PriorityAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_date', 'mod_date', 'last_edited_by')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_date', 'mod_date', 'last_edited_by')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  search_fields = ['name']

class TaskAdmin(admin.ModelAdmin):
  list_display = ('id', 'summary', 'registered', 'author',
                  'assigned_to', 'start_date','priority','status',
                  'complete_date','last_edited', 'last_edited_by')
  exclude = ('last_edited_by',)
  def save_model(self, request, obj, form, change):
      obj.last_edited_by = request.user.username
      obj.save()
  list_filter = ['priority', 'status']
  search_fields = ['author', 'assigned_to', 'summary']

class WorkLogAdmin(admin.ModelAdmin):
  list_display = ('task', 'start_date', 'complete_date', 'assigned_to', 'notes',)

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Priority, PriorityAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.WorkLog, WorkLogAdmin)