from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    TYPE_CHOICES = [
        ('task_deadline', _('Task Deadline')),
        ('exam_reminder', _('Exam Reminder')),
        ('schedule_reminder', _('Schedule Reminder')),
        ('overdue_task', _('Overdue Task')),
        ('goal_reminder', _('Goal Reminder')),
        ('info', _('Information')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(_('Title'), max_length=200)
    message = models.TextField(_('Message'))
    notification_type = models.CharField(_('Type'), max_length=20, choices=TYPE_CHOICES, default='info')
    is_read = models.BooleanField(_('Is Read'), default=False)
    link = models.CharField(_('Link'), max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
