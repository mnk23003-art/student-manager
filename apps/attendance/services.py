from django.db.models import Count, Q
from .models import Attendance


def calculate_attendance_stats(user, semester, subject=None):
    queryset = Attendance.objects.filter(user=user, semester=semester)
    if subject:
        queryset = queryset.filter(subject=subject)

    total = queryset.count()
    if total == 0:
        return None

    present = queryset.filter(status='present').count()
    late = queryset.filter(status='late').count()
    absent = queryset.filter(status='absent').count()
    excused = queryset.filter(status='excused').count()

    attendance_pct = round(((present + late) / total) * 100, 1) if total > 0 else 0

    return {
        'total': total,
        'present': present,
        'late': late,
        'absent': absent,
        'excused': excused,
        'percentage': attendance_pct,
    }


def calculate_subject_attendance(user, semester):
    from apps.subjects.models import Subject
    subjects = Subject.objects.filter(user=user, semester=semester)
    result = []

    for subject in subjects:
        stats = calculate_attendance_stats(user, semester, subject)
        result.append({
            'subject': subject,
            'stats': stats,
        })

    return result
