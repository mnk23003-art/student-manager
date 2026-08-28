from django.db.models import Sum, Avg, Count, F, Q
from decimal import Decimal


def calculate_average_grade(user, semester, subject=None):
    from .models import Grade
    grades = Grade.objects.filter(user=user, semester=semester)
    if subject:
        grades = grades.filter(subject=subject)

    if not grades.exists():
        return None

    total = sum(g.get_percentage() for g in grades)
    return round(total / grades.count(), 1)


def calculate_weighted_average(user, semester, subject=None):
    from .models import Grade
    grades = Grade.objects.filter(user=user, semester=semester)
    if subject:
        grades = grades.filter(subject=subject)

    if not grades.exists():
        return None

    weighted_sum = Decimal('0')
    total_weight = Decimal('0')

    for grade in grades:
        weighted_sum += grade.score * grade.weight
        total_weight += grade.max_score * grade.weight

    if total_weight == 0:
        return 0

    return round(float((weighted_sum / total_weight) * 100), 1)


def calculate_gpa(user, semester, system='percentage'):
    from .models import Grade
    grades = Grade.objects.filter(user=user, semester=semester)

    if not grades.exists():
        return None

    if system == 'gpa-4':
        total = sum(g.get_gpa_4() for g in grades)
        return round(total / grades.count(), 2)
    elif system == '5-point':
        total = sum(g.get_5_point() for g in grades)
        return round(total / grades.count(), 1)
    elif system == '10-point':
        total = sum(g.get_10_point() for g in grades)
        return round(total / grades.count(), 1)
    else:
        return calculate_average_grade(user, semester)


def calculate_subject_grades(user, semester):
    from apps.subjects.models import Subject
    subjects = Subject.objects.filter(user=user, semester=semester)
    result = []

    for subject in subjects:
        avg = calculate_average_grade(user, semester, subject)
        result.append({
            'subject': subject,
            'average': avg,
        })

    return sorted(result, key=lambda x: x['average'] or 0, reverse=True)


def predict_needed_grade(user, semester, subject, desired_average):
    from .models import Grade
    grades = Grade.objects.filter(user=user, semester=semester, subject=subject)

    if not grades.exists():
        return {'possible': True, 'needed': desired_average}

    current_total = sum(g.get_percentage() for g in grades)
    current_count = grades.count()

    target_total = desired_average * (current_count + 1)
    needed = target_total - current_total

    if needed < 0:
        needed = 0

    if needed > 100:
        return {'possible': False, 'message': 'Your target is currently unreachable.'}

    return {'possible': True, 'needed': round(needed, 1)}
