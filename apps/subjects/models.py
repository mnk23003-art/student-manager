from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subjects')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(_('Subject Name'), max_length=200)
    teacher = models.CharField(_('Teacher'), max_length=200, blank=True)
    room = models.CharField(_('Room'), max_length=100, blank=True)
    credits = models.PositiveIntegerField(_('Credits'), default=0)
    hours = models.PositiveIntegerField(_('Hours'), default=0)
    color = models.CharField(_('Color'), max_length=7, default='#3B82F6')
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_average_grade(self):
        from apps.grades.models import Grade
        grades = Grade.objects.filter(user=self.user, subject=self, semester=self.semester)
        if not grades.exists():
            return None
        total = sum(g.get_percentage() for g in grades)
        return round(total / grades.count(), 1)
    
    def get_attendance_percentage(self):
        from apps.attendance.models import Attendance
        records = Attendance.objects.filter(user=self.user, subject=self)
        if not records.exists():
            return None
        present = records.filter(status='present').count() + records.filter(status='late').count()
        return round((present / records.count()) * 100, 1)
    
    def get_overdue_tasks_count(self):
        from apps.tasks.models import Task
        from django.utils import timezone
        return Task.objects.filter(
            user=self.user, subject=self, semester=self.semester,
            deadline__lt=timezone.now(), status__in=['todo', 'in_progress']
        ).count()
    
    def get_upcoming_tasks(self, limit=5):
        from apps.tasks.models import Task
        from django.utils import timezone
        return Task.objects.filter(
            user=self.user, subject=self, semester=self.semester,
            deadline__gte=timezone.now(), status__in=['todo', 'in_progress']
        ).order_by('deadline')[:limit]
