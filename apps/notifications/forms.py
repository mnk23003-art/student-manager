from django import forms


class NotificationSettingsForm(forms.Form):
    task_reminders = forms.BooleanField(required=False, initial=True, label='Task Reminders')
    exam_reminders = forms.BooleanField(required=False, initial=True, label='Exam Reminders')
    schedule_reminders = forms.BooleanField(required=False, initial=True, label='Schedule Reminders')
    overdue_reminders = forms.BooleanField(required=False, initial=True, label='Overdue Reminders')
