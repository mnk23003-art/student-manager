from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['subject', 'date', 'status', 'user']
    list_filter = ['status', 'semester']
    search_fields = ['subject__name']
