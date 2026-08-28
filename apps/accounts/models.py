from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username
    
    def get_full_name_display(self):
        full = self.get_full_name()
        return full if full else self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    university = models.CharField(_('University'), max_length=200, blank=True)
    faculty = models.CharField(_('Faculty'), max_length=200, blank=True)
    specialization = models.CharField(_('Specialization'), max_length=200, blank=True)
    course = models.PositiveIntegerField(_('Course'), null=True, blank=True)
    academic_year = models.CharField(_('Academic Year'), max_length=20, blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    
    class Meta:
        verbose_name = _('Student Profile')
        verbose_name_plural = _('Student Profiles')
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def get_initials(self):
        first = self.user.first_name[:1] if self.user.first_name else ''
        last = self.user.last_name[:1] if self.user.last_name else ''
        return (first + last).upper() or self.user.username[:2].upper()


class UserSettings(models.Model):
    GRADING_CHOICES = [
        ('percentage', 'Percentage'),
        ('5-point', '5-Point'),
        ('10-point', '10-Point'),
        ('gpa-4', 'GPA 4.0'),
    ]
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System'),
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ru', 'Russian'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    grading_system = models.CharField(max_length=20, choices=GRADING_CHOICES, default='percentage')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='system')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    task_reminders = models.BooleanField(default=True)
    exam_reminders = models.BooleanField(default=True)
    schedule_reminders = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')
    
    def __str__(self):
        return f"Settings for {self.user.username}"
