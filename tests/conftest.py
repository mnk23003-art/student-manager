import pytest
from django.test import TestCase
from apps.accounts.models import User, StudentProfile, UserSettings
from apps.semesters.models import Semester
from apps.subjects.models import Subject
from apps.tasks.models import Task
from apps.grades.models import Grade
from apps.attendance.models import Attendance
from apps.exams.models import Exam
from apps.notes.models import Note
from apps.goals.models import Goal
from apps.schedule.models import ScheduleItem
from apps.calendar.models import CalendarEvent
from apps.productivity.models import FocusSession
from apps.notifications.models import Notification
from datetime import date, time, timedelta
from django.utils import timezone


@pytest.fixture
def user(db):
    u = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    StudentProfile.objects.create(user=u, university='Test Uni', faculty='CS')
    UserSettings.objects.create(user=u)
    return u


@pytest.fixture
def user2(db):
    return User.objects.create_user(username='user2', email='user2@example.com', password='pass1234')


@pytest.fixture
def semester(user):
    return Semester.objects.create(
        user=user,
        name='Test Semester',
        academic_year='2026/2027',
        start_date=date.today() - timedelta(days=30),
        end_date=date.today() + timedelta(days=120),
        is_active=True
    )


@pytest.fixture
def subject(user, semester):
    return Subject.objects.create(
        user=user,
        semester=semester,
        name='Mathematics',
        teacher='Dr. Smith',
        room='Room 101',
        credits=4,
        color='#3B82F6'
    )


@pytest.fixture
def task(user, semester, subject):
    return Task.objects.create(
        user=user,
        semester=semester,
        subject=subject,
        title='Test Task',
        deadline=timezone.now() + timedelta(days=5),
        priority='medium',
        status='todo',
        estimated_time=60
    )


@pytest.fixture
def grade(user, semester, subject):
    return Grade.objects.create(
        user=user,
        semester=semester,
        subject=subject,
        title='Test Grade',
        grade_type='homework',
        score=85,
        max_score=100,
        weight=20,
        date=date.today()
    )


@pytest.fixture
def attendance(user, semester, subject):
    return Attendance.objects.create(
        user=user,
        semester=semester,
        subject=subject,
        date=date.today(),
        status='present'
    )


@pytest.fixture
def exam(user, semester, subject):
    return Exam.objects.create(
        user=user,
        semester=semester,
        subject=subject,
        title='Final Exam',
        date=date.today() + timedelta(days=10),
        time=time(10, 0),
        location='Room 201'
    )


@pytest.fixture
def note(user, semester, subject):
    return Note.objects.create(
        user=user,
        semester=semester,
        subject=subject,
        title='Test Note',
        content='Test content',
        tags='test,notes'
    )


@pytest.fixture
def goal(user, semester):
    return Goal.objects.create(
        user=user,
        semester=semester,
        title='Test Goal',
        description='Test description',
        target='Achieve target',
        progress=50,
        deadline=date.today() + timedelta(days=30),
        status='in_progress'
    )
