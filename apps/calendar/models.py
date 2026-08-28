from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CalendarEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('class', _('Class')),
        ('task', _('Task')),
        ('exam', _('Exam')),
        ('event', _('Event')),
        ('other', _('Other')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendar_events')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='calendar_events')
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    date = models.DateField(_('Date'))
    start_time = models.TimeField(_('Start Time'), null=True, blank=True)
    end_time = models.TimeField(_('End Time'), null=True, blank=True)
    event_type = models.CharField(_('Event Type'), max_length=20, choices=EVENT_TYPE_CHOICES, default='event')
    color = models.CharField(_('Color'), max_length=7, default='#3B82F6')
    is_all_day = models.BooleanField(_('All Day'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Calendar Event')
        verbose_name_plural = _('Calendar Events')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.date}"
