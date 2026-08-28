from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Grade(models.Model):
    GRADE_TYPE_CHOICES = [
        ('homework', _('Homework')),
        ('quiz', _('Quiz')),
        ('test', _('Test')),
        ('midterm', _('Midterm')),
        ('exam', _('Exam')),
        ('project', _('Project')),
        ('other', _('Other')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grades')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='grades')
    title = models.CharField(_('Title'), max_length=200)
    grade_type = models.CharField(_('Grade Type'), max_length=20, choices=GRADE_TYPE_CHOICES, default='homework')
    score = models.DecimalField(_('Score'), max_digits=6, decimal_places=2)
    max_score = models.DecimalField(_('Max Score'), max_digits=6, decimal_places=2, default=100)
    weight = models.DecimalField(_('Weight (%)'), max_digits=5, decimal_places=2, default=1.0)
    date = models.DateField(_('Date'), default=timezone.now)
    comment = models.TextField(_('Comment'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Grade')
        verbose_name_plural = _('Grades')
        ordering = ['-date']

    def __str__(self):
        return f"{self.title}: {self.score}/{self.max_score}"

    def get_percentage(self):
        if self.max_score == 0:
            return 0
        return round((float(self.score) / float(self.max_score)) * 100, 1)

    def get_gpa_4(self):
        pct = self.get_percentage()
        if pct >= 93:
            return 4.0
        elif pct >= 90:
            return 3.7
        elif pct >= 87:
            return 3.3
        elif pct >= 83:
            return 3.0
        elif pct >= 80:
            return 2.7
        elif pct >= 77:
            return 2.3
        elif pct >= 73:
            return 2.0
        elif pct >= 70:
            return 1.7
        elif pct >= 67:
            return 1.3
        elif pct >= 63:
            return 1.0
        elif pct >= 60:
            return 0.7
        else:
            return 0.0

    def get_5_point(self):
        pct = self.get_percentage()
        if pct >= 90:
            return 5
        elif pct >= 73:
            return 4
        elif pct >= 55:
            return 3
        elif pct >= 40:
            return 2
        else:
            return 1

    def get_10_point(self):
        pct = self.get_percentage()
        if pct >= 95:
            return 10
        elif pct >= 85:
            return 9
        elif pct >= 75:
            return 8
        elif pct >= 65:
            return 7
        elif pct >= 55:
            return 6
        elif pct >= 45:
            return 5
        elif pct >= 35:
            return 4
        elif pct >= 25:
            return 3
        elif pct >= 15:
            return 2
        else:
            return 1
