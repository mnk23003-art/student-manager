from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class FocusSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='focus_sessions')
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='focus_sessions')
    start_time = models.DateTimeField(_('Start Time'))
    end_time = models.DateTimeField(_('End Time'), null=True, blank=True)
    duration = models.PositiveIntegerField(_('Duration (seconds)'), default=0)
    completed = models.BooleanField(_('Completed'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Focus Session')
        verbose_name_plural = _('Focus Sessions')
        ordering = ['-start_time']
    
    def __str__(self):
        task_name = self.task.title if self.task else 'No task'
        return f"{task_name} - {self.duration // 60}min"
    
    def is_active(self):
        return self.end_time is None
    
    def get_duration_display(self):
        mins = self.duration // 60
        secs = self.duration % 60
        if mins > 0:
            return f"{mins}m {secs}s"
        return f"{secs}s"


class PomodoroSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pomodoro_settings')
    focus_duration = models.PositiveIntegerField(_('Focus Duration (minutes)'), default=25)
    short_break = models.PositiveIntegerField(_('Short Break (minutes)'), default=5)
    long_break = models.PositiveIntegerField(_('Long Break (minutes)'), default=15)
    sessions_before_long = models.PositiveIntegerField(_('Sessions Before Long Break'), default=4)
    
    class Meta:
        verbose_name = _('Pomodoro Settings')
        verbose_name_plural = _('Pomodoro Settings')
    
    def __str__(self):
        return f"Pomodoro: {self.focus_duration}min focus"
