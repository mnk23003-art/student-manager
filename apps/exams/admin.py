from django.contrib import admin
from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'date', 'time', 'location', 'user']
    list_filter = ['date', 'semester']
    search_fields = ['title', 'subject__name']
