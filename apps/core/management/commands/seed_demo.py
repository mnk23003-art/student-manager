import random
from datetime import timedelta, time, date
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User, StudentProfile, UserSettings
from apps.semesters.models import Semester
from apps.subjects.models import Subject
from apps.schedule.models import ScheduleItem
from apps.tasks.models import Task
from apps.grades.models import Grade
from apps.attendance.models import Attendance
from apps.exams.models import Exam
from apps.notes.models import Note
from apps.goals.models import Goal
from apps.calendar.models import CalendarEvent
from apps.productivity.models import FocusSession, PomodoroSettings
from apps.notifications.models import Notification


class Command(BaseCommand):
    help = 'Create demo data for Student Manager'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')
        
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Alex',
                'last_name': 'Johnson',
            }
        )
        if created:
            user.set_password('demo1234')
            user.save()
        
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        profile.university = 'MIT'
        profile.faculty = 'Computer Science'
        profile.specialization = 'Software Engineering'
        profile.course = 3
        profile.academic_year = '2026/2027'
        profile.save()
        
        settings_obj, _ = UserSettings.objects.get_or_create(user=user)
        settings_obj.grading_system = 'percentage'
        settings_obj.save()
        
        pom_settings, _ = PomodoroSettings.objects.get_or_create(user=user)
        
        today = timezone.now().date()
        
        sem1, _ = Semester.objects.get_or_create(
            user=user, name='Semester 1', academic_year='2026/2027',
            defaults={'start_date': today - timedelta(days=60), 'end_date': today + timedelta(days=120), 'is_active': True}
        )
        sem2, _ = Semester.objects.get_or_create(
            user=user, name='Semester 2', academic_year='2026/2027',
            defaults={'start_date': today + timedelta(days=125), 'end_date': today + timedelta(days=240), 'is_active': False}
        )
        
        subjects_data = [
            ('Mathematics', 'Dr. Smith', 'Room 101', 4, 60, '#3B82F6'),
            ('Programming', 'Prof. Davis', 'Lab 202', 5, 80, '#10B981'),
            ('English', 'Ms. Brown', 'Room 303', 3, 45, '#F59E0B'),
            ('Physics', 'Dr. Wilson', 'Lab 105', 4, 60, '#8B5CF6'),
            ('Database Systems', 'Prof. Taylor', 'Lab 201', 4, 70, '#EF4444'),
            ('Web Development', 'Ms. Anderson', 'Lab 301', 3, 50, '#06B6D4'),
            ('Algorithms', 'Dr. Thomas', 'Room 102', 4, 60, '#EC4899'),
            ('Statistics', 'Prof. Jackson', 'Room 205', 3, 45, '#84CC16'),
        ]
        
        subjects = []
        for name, teacher, room, credits, hours, color in subjects_data:
            s, _ = Subject.objects.get_or_create(
                user=user, semester=sem1, name=name,
                defaults={'teacher': teacher, 'room': room, 'credits': credits, 'hours': hours, 'color': color}
            )
            subjects.append(s)
        
        days = [0, 1, 2, 3, 4]
        times = [(time(9, 0), time(10, 30)), (time(11, 0), time(12, 30)), (time(14, 0), time(15, 30)), (time(16, 0), time(17, 0))]
        lesson_types = ['lecture', 'seminar', 'laboratory', 'practice']
        
        for i, subject in enumerate(subjects[:5]):
            day = days[i % len(days)]
            start, end = times[i % len(times)]
            ScheduleItem.objects.get_or_create(
                user=user, subject=subject, semester=sem1, day_of_week=day,
                defaults={'start_time': start, 'end_time': end, 'lesson_type': random.choice(lesson_types), 'room': subject.room, 'teacher': subject.teacher}
            )
        
        task_titles = [
            'Python Project', 'Math Homework', 'English Essay', 'Physics Lab Report',
            'Database Assignment', 'Web Design Project', 'Algorithm Analysis', 'Statistics Problem Set',
            'Read Chapter 5', 'Review Lecture Notes', 'Practice Problems', 'Group Discussion Prep',
            'Research Paper Outline', 'Code Review', 'Final Project Planning', 'Midterm Study Guide',
            'Lab Exercise 3', 'Worksheet Problems', 'Online Quiz Prep', 'Presentation Slides',
            'Study Session Notes', 'Concept Map', 'Flashcards Creation', 'Mock Exam',
            'Assignment Review', 'Peer Code Review', 'Documentation Update', 'Test Cases Writing',
            'Project Proposal', 'Literature Review'
        ]
        
        priorities = ['low', 'medium', 'high', 'urgent']
        statuses = ['todo', 'in_progress', 'completed']
        
        for i, title in enumerate(task_titles):
            days_offset = random.randint(-5, 14)
            deadline = timezone.now() + timedelta(days=days_offset, hours=random.randint(0, 23))
            status = random.choice(statuses)
            subject = random.choice(subjects) if random.random() > 0.2 else None
            
            Task.objects.get_or_create(
                user=user, semester=sem1, title=title,
                defaults={
                    'subject': subject,
                    'deadline': deadline,
                    'priority': random.choice(priorities),
                    'status': status,
                    'estimated_time': random.choice([15, 30, 45, 60, 90, 120, 180]),
                    'completed_at': timezone.now() - timedelta(days=random.randint(1, 10)) if status == 'completed' else None,
                }
            )
        
        grade_types = ['homework', 'quiz', 'test', 'midterm', 'exam', 'project']
        for subject in subjects:
            for i in range(5):
                score = random.randint(60, 100)
                Grade.objects.get_or_create(
                    user=user, semester=sem1, subject=subject,
                    title=f'{subject.name} {random.choice(grade_types).title()} {i+1}',
                    defaults={
                        'grade_type': random.choice(grade_types),
                        'score': score,
                        'max_score': 100,
                        'weight': random.choice([10, 15, 20, 25]),
                        'date': today - timedelta(days=random.randint(1, 45)),
                    }
                )
        
        for subject in subjects:
            for i in range(15):
                att_date = today - timedelta(days=random.randint(0, 30))
                if att_date.weekday() < 5:
                    Attendance.objects.get_or_create(
                        user=user, subject=subject, date=att_date,
                        defaults={
                            'semester': sem1,
                            'status': random.choices(['present', 'absent', 'late', 'excused'], weights=[70, 15, 10, 5])[0],
                        }
                    )
        
        exam_data = [
            ('Midterm Exam', 5), ('Final Exam', 30), ('Quiz 1', 2), ('Practical Exam', 10), ('Oral Exam', 20),
        ]
        for i, (title, days_offset) in enumerate(exam_data):
            Exam.objects.get_or_create(
                user=user, semester=sem1, title=title,
                defaults={
                    'subject': subjects[i % len(subjects)],
                    'date': today + timedelta(days=days_offset),
                    'time': time(10, 0),
                    'location': f'Room {random.randint(100, 500)}',
                    'description': f'{title} covering chapters {i+1}-{i+3}',
                }
            )
        
        notes_data = [
            ('Python Decorators', 'Notes on decorators, closures, and @syntax.'),
            ('SQL Joins', 'INNER JOIN, LEFT JOIN, RIGHT JOIN examples.'),
            ('React Hooks', 'useState, useEffect, custom hooks.'),
            ('Algorithms', 'Binary search, quicksort, merge sort.'),
            ('Statistics Formulas', 'Mean, median, mode, standard deviation.'),
        ]
        for title, content in notes_data:
            Note.objects.get_or_create(
                user=user, semester=sem1, title=title,
                defaults={
                    'content': content,
                    'subject': random.choice(subjects),
                    'tags': 'programming,notes',
                }
            )
        
        goals_data = [
            ('GPA above 4.0', 'Maintain excellent grades', 'Achieve 4.0+ GPA'),
            ('90% Attendance', 'Attend all classes', '90%+ attendance rate'),
            ('Complete Python Course', 'Finish online Python course', 'Python certification'),
            ('Read 5 Books', 'Read academic and technical books', '5 books completed'),
            ('Portfolio Project', 'Build a web application portfolio', 'Deploy to production'),
        ]
        for title, desc, target in goals_data:
            Goal.objects.get_or_create(
                user=user, semester=sem1, title=title,
                defaults={
                    'description': desc,
                    'target': target,
                    'progress': random.randint(0, 80),
                    'status': random.choice(['not_started', 'in_progress', 'completed']),
                    'deadline': today + timedelta(days=random.randint(10, 90)),
                }
            )
        
        event_types = ['event', 'other']
        for i in range(8):
            CalendarEvent.objects.get_or_create(
                user=user, semester=sem1, title=f'Event {i+1}',
                defaults={
                    'date': today + timedelta(days=random.randint(-3, 14)),
                    'event_type': random.choice(event_types),
                    'color': random.choice(['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']),
                }
            )
        
        for i in range(10):
            FocusSession.objects.get_or_create(
                user=user,
                start_time=timezone.now() - timedelta(days=random.randint(0, 7), hours=random.randint(1, 8)),
                defaults={
                    'task': random.choice(Task.objects.filter(user=user)[:5]) if Task.objects.filter(user=user).exists() else None,
                    'duration': random.randint(900, 3600),
                    'completed': True,
                }
            )
        
        notifications_data = [
            ('Task Overdue', 'Python Project is overdue!', 'overdue_task'),
            ('Exam Coming', 'Midterm Exam in 5 days', 'exam_reminder'),
            ('Welcome', 'Welcome to Student Manager!', 'info'),
        ]
        for title, msg, ntype in notifications_data:
            Notification.objects.get_or_create(
                user=user, title=title,
                defaults={'message': msg, 'notification_type': ntype}
            )
        
        self.stdout.write(self.style.SUCCESS('Demo data created successfully!'))
        self.stdout.write(f'Login: demo / demo1234')
