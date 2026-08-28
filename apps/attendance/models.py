from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', _('Present')),
        ('absent', _('Absent')),
        ('late', _('Late')),
        ('excused', _('Excused')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='attendances')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(_('Date'), default=timezone.now)
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='present')
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subject', 'date'],
                name='unique_attendance_per_subject_per_day'
            )
        ]

    def __str__(self):
        return f"{self.subject.name} - {self.date} - {self.get_status_display()}"
