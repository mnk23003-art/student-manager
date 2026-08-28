from django.contrib import admin
from .models import CalendarEvent

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'event_type', 'user']
    list_filter = ['event_type', 'date']
    search_fields = ['title']
