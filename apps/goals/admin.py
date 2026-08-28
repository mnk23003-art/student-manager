from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'progress', 'deadline', 'user']
    list_filter = ['status', 'semester']
    search_fields = ['title']
