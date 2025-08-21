from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'assigned_to', 'start_date', 'end_date', 'is_completed')
    search_fields = ('task_name', 'details', 'assigned_to__username')
    list_filter = ('is_completed', 'start_date', 'end_date')
