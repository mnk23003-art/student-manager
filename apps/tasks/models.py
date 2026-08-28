from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    STATUS_CHOICES = [
        ('todo', _('To Do')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='tasks')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    deadline = models.DateTimeField(_('Deadline'), null=True, blank=True)
    priority = models.CharField(_('Priority'), max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(_('Status'), max_length=15, choices=STATUS_CHOICES, default='todo')
    estimated_time = models.PositiveIntegerField(_('Estimated Time (minutes)'), null=True, blank=True)
    actual_time = models.PositiveIntegerField(_('Actual Time (minutes)'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        if self.deadline and self.status != 'completed':
            return self.deadline < timezone.now()
        return False
    
    def is_due_today(self):
        if not self.deadline:
            return False
        today = timezone.now().date()
        return self.deadline.date() == today
    
    def is_due_tomorrow(self):
        if not self.deadline:
            return False
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        return self.deadline.date() == tomorrow
    
    def days_until_deadline(self):
        if not self.deadline:
            return None
        delta = self.deadline.date() - timezone.now().date()
        return delta.days
    
    def complete(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def get_estimated_hours(self):
        if self.estimated_time:
            hours = self.estimated_time // 60
            mins = self.estimated_time % 60
            if hours > 0:
                return f"{hours}h {mins}m" if mins else f"{hours}h"
            return f"{mins}m"
        return None
