from django.contrib import admin
from .models import FocusSession, PomodoroSettings

@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ['task', 'duration', 'completed', 'start_time', 'user']
    list_filter = ['completed']
    search_fields = ['task__title']

@admin.register(PomodoroSettings)
class PomodoroSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'focus_duration', 'short_break', 'long_break']
