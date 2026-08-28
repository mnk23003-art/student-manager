from datetime import datetime, timedelta
from django.utils import timezone


def get_week_dates(dt=None):
    if dt is None:
        dt = timezone.now().date()
    start = dt - timedelta(days=dt.weekday())
    return [start + timedelta(days=i) for i in range(7)]


def get_today():
    return timezone.now().date()


def get_days_until(target_date):
    today = get_today()
    if isinstance(target_date, datetime):
        target_date = target_date.date()
    return (target_date - today).days


def calculate_percentage(score, max_score):
    if max_score == 0:
        return 0
    return round((score / max_score) * 100, 2)
