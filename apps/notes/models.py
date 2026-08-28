from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='notes')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    title = models.CharField(_('Title'), max_length=200)
    content = models.TextField(_('Content'))
    tags = models.CharField(_('Tags'), max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_safe_content(self):
        return escape(self.content)