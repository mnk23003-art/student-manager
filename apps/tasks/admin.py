from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'priority', 'status', 'deadline', 'user']
    list_filter = ['status', 'priority', 'semester']
    search_fields = ['title', 'description']
