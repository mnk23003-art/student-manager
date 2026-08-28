import pytest
from django.test import Client
from django.urls import reverse
from apps.tasks.models import Task
from apps.grades.models import Grade
from apps.notes.models import Note
from apps.semesters.models import Semester
from apps.subjects.models import Subject
from datetime import date, timedelta
from django.utils import timezone


@pytest.mark.django_db
class TestUserIsolation:
    def test_user_a_tasks_not_visible_to_user_b(self, client, user, user2, task):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('tasks:list'))
        assert task.title not in str(response.content)

    def test_user_a_grades_not_visible_to_user_b(self, client, user, user2, grade):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('grades:list'))
        assert grade.title not in str(response.content)

    def test_user_a_notes_not_visible_to_user_b(self, client, user, user2, note):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('notes:list'))
        assert note.title not in str(response.content)

    def test_user_a_subjects_not_visible_to_user_b(self, client, user, user2, subject):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('subjects:list'))
        assert subject.name not in str(response.content)

    def test_user_cannot_complete_other_user_task(self, client, user, user2, task):
        client.login(username='user2', password='pass1234')
        response = client.post(reverse('tasks:complete', args=[task.pk]))
        task.refresh_from_db()
        assert task.status == 'todo'

    def test_user_cannot_update_other_user_task(self, client, user, user2, task):
        client.login(username='user2', password='pass1234')
        data = {
            'title': 'Hacked Task',
            'description': '',
            'subject': '',
            'deadline': task.deadline.strftime('%Y-%m-%dT%H:%M'),
            'priority': 'low',
            'status': 'completed',
            'estimated_time': 0,
        }
        response = client.post(reverse('tasks:update', args=[task.pk]), data)
        task.refresh_from_db()
        assert task.title != 'Hacked Task'
