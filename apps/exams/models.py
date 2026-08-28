from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Exam(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='exams')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(_('Title'), max_length=200)
    date = models.DateField(_('Date'))
    time = models.TimeField(_('Time'), null=True, blank=True)
    location = models.CharField(_('Location'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.date}"

    def days_until(self):
        today = timezone.now().date()
        delta = self.date - today
        return max(delta.days, 0)

    def is_upcoming(self):
        return self.date >= timezone.now().date()

    def is_today(self):
        return self.date == timezone.now().date()

    def is_past(self):
        return self.date < timezone.now().date()
