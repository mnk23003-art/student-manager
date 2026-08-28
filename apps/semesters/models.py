from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Semester(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(_('Semester Name'), max_length=100)
    academic_year = models.CharField(_('Academic Year'), max_length=20)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    is_active = models.BooleanField(_('Is Active'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Semester')
        verbose_name_plural = _('Semesters')
        ordering = ['-start_date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'is_active'],
                condition=models.Q(is_active=True),
                name='unique_active_semester_per_user'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

    def save(self, *args, **kwargs):
        if self.is_active:
            Semester.objects.filter(
                user=self.user, is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def get_progress(self):
        today = timezone.now().date()
        total_days = (self.end_date - self.start_date).days
        if total_days <= 0:
            return 0
        elapsed = (today - self.start_date).days
        return min(max(int((elapsed / total_days) * 100), 0), 100)

    def days_left(self):
        today = timezone.now().date()
        delta = self.end_date - today
        return max(delta.days, 0)

    def is_current(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date
