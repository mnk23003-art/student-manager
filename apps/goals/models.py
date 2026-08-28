from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Goal(models.Model):
    STATUS_CHOICES = [
        ('not_started', _('Not Started')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    target = models.CharField(_('Target'), max_length=200, blank=True)
    progress = models.PositiveIntegerField(_('Progress (%)'), default=0)
    deadline = models.DateField(_('Deadline'), null=True, blank=True)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_overdue(self):
        if self.deadline and self.status != 'completed':
            return self.deadline < timezone.now().date()
        return False

    def days_until_deadline(self):
        if not self.deadline:
            return None
        delta = self.deadline - timezone.now().date()
        return delta.days
