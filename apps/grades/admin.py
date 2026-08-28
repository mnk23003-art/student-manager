from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'score', 'max_score', 'grade_type', 'date', 'user']
    list_filter = ['grade_type', 'semester']
    search_fields = ['title', 'subject__name']
