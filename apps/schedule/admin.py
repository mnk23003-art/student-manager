from django.contrib import admin
from .models import ScheduleItem

@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ['subject', 'day_of_week', 'start_time', 'end_time', 'lesson_type', 'user']
    list_filter = ['day_of_week', 'lesson_type', 'semester']
    search_fields = ['subject__name', 'teacher', 'room']
