from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ScheduleItem(models.Model):
    DAY_CHOICES = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]
    LESSON_TYPE_CHOICES = [
        ('lecture', _('Lecture')),
        ('seminar', _('Seminar')),
        ('laboratory', _('Laboratory')),
        ('practice', _('Practice')),
        ('other', _('Other')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='schedule_items')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='schedule_items')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='schedule_items')
    day_of_week = models.IntegerField(_('Day of Week'), choices=DAY_CHOICES)
    start_time = models.TimeField(_('Start Time'))
    end_time = models.TimeField(_('End Time'))
    lesson_type = models.CharField(_('Lesson Type'), max_length=20, choices=LESSON_TYPE_CHOICES, default='lecture')
    teacher = models.CharField(_('Teacher'), max_length=200, blank=True)
    room = models.CharField(_('Room'), max_length=100, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Schedule Item')
        verbose_name_plural = _('Schedule Items')
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.subject.name} - {self.get_day_of_week_display()} {self.start_time}"
    
    def get_day_display(self):
        return self.get_day_of_week_display()
    
    def has_conflict(self):
        overlapping = ScheduleItem.objects.filter(
            user=self.user,
            semester=self.semester,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)
        return overlapping.exists()
    
    def get_conflicting_items(self):
        return ScheduleItem.objects.filter(
            user=self.user,
            semester=self.semester,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)
