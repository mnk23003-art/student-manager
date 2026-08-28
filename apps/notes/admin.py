from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created_at', 'user']
    list_filter = ['semester']
    search_fields = ['title', 'content', 'tags']