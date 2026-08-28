import csv
import io
from datetime import datetime, date
from django.http import HttpResponse
from django.utils import timezone


def export_to_csv(queryset, fields, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'

    writer = csv.writer(response)
    writer.writerow([f.replace('_', ' ').title() for f in fields])

    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field, '')
            if isinstance(value, (datetime, date)):
                value = value.strftime('%Y-%m-%d')
            elif hasattr(value, 'pk'):
                value = str(value)
            row.append(value)
        writer.writerow(row)

    return response


def export_tasks_to_csv(queryset):
    fields = ['title', 'subject', 'deadline', 'priority', 'status', 'estimated_time', 'created_at']
    return export_to_csv(queryset, fields, 'tasks')


def export_grades_to_csv(queryset):
    fields = ['title', 'subject', 'grade_type', 'score', 'max_score', 'weight', 'date']
    return export_to_csv(queryset, fields, 'grades')


def export_attendance_to_csv(queryset):
    fields = ['subject', 'date', 'status', 'notes']
    return export_to_csv(queryset, fields, 'attendance')


def export_schedule_to_csv(queryset):
    fields = ['subject', 'day_of_week', 'start_time', 'end_time', 'lesson_type', 'teacher', 'room']
    return export_to_csv(queryset, fields, 'schedule')


def export_tasks_to_xlsx(queryset):
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Tasks"

    headers = ['Title', 'Subject', 'Deadline', 'Priority', 'Status', 'Estimated Time', 'Created']
    ws.append(headers)

    for task in queryset:
        ws.append([
            task.title,
            task.subject.name if task.subject else '',
            task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else '',
            task.get_priority_display(),
            task.get_status_display(),
            task.estimated_time or '',
            task.created_at.strftime('%Y-%m-%d'),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="tasks_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    wb.save(response)
    return response


def export_grades_to_xlsx(queryset):
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Grades"

    headers = ['Title', 'Subject', 'Type', 'Score', 'Max Score', 'Weight', 'Date', 'Percentage']
    ws.append(headers)

    for grade in queryset:
        ws.append([
            grade.title,
            grade.subject.name if grade.subject else '',
            grade.get_grade_type_display(),
            float(grade.score),
            float(grade.max_score),
            float(grade.weight),
            grade.date.strftime('%Y-%m-%d'),
            grade.get_percentage(),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="grades_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    wb.save(response)
    return response


def export_grades_to_pdf(queryset, user):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=20)

    elements = []
    elements.append(Paragraph(f"Grades Report - {user.get_full_name_display()}", title_style))
    elements.append(Paragraph(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    data = [['Title', 'Subject', 'Type', 'Score', 'Max', 'Weight', 'Date']]
    for grade in queryset:
        data.append([
            grade.title,
            grade.subject.name if grade.subject else '',
            grade.get_grade_type_display(),
            str(grade.score),
            str(grade.max_score),
            f'{grade.weight}%',
            grade.date.strftime('%Y-%m-%d'),
        ])

    table = Table(data, colWidths=[120, 80, 60, 50, 40, 50, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F4F6')]),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="grades_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    return response


def parse_csv_upload(file_content):
    reader = csv.DictReader(io.StringIO(file_content))
    rows = []
    errors = []

    for i, row in enumerate(reader, 1):
        try:
            rows.append(row)
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")

    return rows, errors


def import_tasks_from_csv(file_content, user, semester):
    from apps.tasks.models import Task
    from apps.subjects.models import Subject

    rows, errors = parse_csv_upload(file_content)
    imported = 0

    for row in rows:
        try:
            subject = None
            subject_name = row.get('subject', '').strip()
            if subject_name:
                subject = Subject.objects.filter(user=user, semester=semester, name__icontains=subject_name).first()

            deadline = None
            deadline_str = row.get('deadline', '').strip()
            if deadline_str:
                try:
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
                    deadline = timezone.make_aware(deadline)
                except ValueError:
                    try:
                        deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                        deadline = timezone.make_aware(deadline)
                    except ValueError:
                        errors.append(f"Invalid deadline format: {deadline_str}")

            Task.objects.create(
                user=user,
                semester=semester,
                title=row.get('title', 'Untitled'),
                subject=subject,
                deadline=deadline,
                priority=row.get('priority', 'medium').lower(),
                status=row.get('status', 'todo').lower(),
                estimated_time=int(row.get('estimated_time', 0) or 0),
            )
            imported += 1
        except Exception as e:
            errors.append(f"Error importing task: {str(e)}")

    return imported, errors


def import_grades_from_csv(file_content, user, semester):
    from apps.grades.models import Grade
    from apps.subjects.models import Subject

    rows, errors = parse_csv_upload(file_content)
    imported = 0

    for row in rows:
        try:
            subject = None
            subject_name = row.get('subject', '').strip()
            if subject_name:
                subject = Subject.objects.filter(user=user, semester=semester, name__icontains=subject_name).first()

            grade_date = date.today()
            date_str = row.get('date', '').strip()
            if date_str:
                try:
                    grade_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass

            Grade.objects.create(
                user=user,
                semester=semester,
                subject=subject,
                title=row.get('title', 'Untitled'),
                grade_type=row.get('grade_type', 'other').lower(),
                score=float(row.get('score', 0) or 0),
                max_score=float(row.get('max_score', 100) or 100),
                weight=float(row.get('weight', 1) or 1),
                date=grade_date,
            )
            imported += 1
        except Exception as e:
            errors.append(f"Error importing grade: {str(e)}")

    return imported, errors
