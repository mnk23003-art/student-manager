from django.contrib import admin
from .models import Semester

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'academic_year', 'user', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'academic_year']
    search_fields = ['name', 'user__username']
