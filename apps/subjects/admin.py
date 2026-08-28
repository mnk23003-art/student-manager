from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'semester', 'credits', 'user']
    list_filter = ['semester']
    search_fields = ['name', 'teacher']
