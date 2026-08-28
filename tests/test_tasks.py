import pytest
from django.test import Client
from django.urls import reverse
from apps.tasks.models import Task
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestTasks:
    def test_task_list(self, client, user, task):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('tasks:list'))
        assert response.status_code == 200

    def test_task_create(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Task',
            'description': '',
            'subject': subject.pk,
            'deadline': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M'),
            'priority': 'high',
            'status': 'todo',
            'estimated_time': 30,
        }
        response = client.post(reverse('tasks:create'), data)
        assert response.status_code == 302
        assert Task.objects.filter(title='New Task').exists()

    def test_task_detail(self, client, user, task):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('tasks:detail', args=[task.pk]))
        assert response.status_code == 200

    def test_task_update(self, client, user, task):
        client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Updated Task',
            'description': '',
            'subject': task.subject.pk,
            'deadline': task.deadline.strftime('%Y-%m-%dT%H:%M'),
            'priority': 'urgent',
            'status': 'in_progress',
            'estimated_time': 90,
        }
        response = client.post(reverse('tasks:update', args=[task.pk]), data)
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.title == 'Updated Task'

    def test_task_delete(self, client, user, task):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('tasks:delete', args=[task.pk]))
        assert response.status_code == 302
        assert not Task.objects.filter(pk=task.pk).exists()

    def test_task_complete(self, client, user, task):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('tasks:complete', args=[task.pk]))
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.status == 'completed'
        assert task.completed_at is not None

    def test_task_is_overdue(self, user, semester):
        task = Task.objects.create(
            user=user, semester=semester, title='Overdue Task',
            deadline=timezone.now() - timedelta(days=1),
            priority='medium', status='todo'
        )
        assert task.is_overdue() is True

    def test_task_is_not_overdue_when_completed(self, user, semester):
        task = Task.objects.create(
            user=user, semester=semester, title='Done Task',
            deadline=timezone.now() - timedelta(days=1),
            priority='medium', status='completed'
        )
        assert task.is_overdue() is False

    def test_task_filter_by_status(self, client, user, task):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('tasks:list') + '?status=todo')
        assert response.status_code == 200

    def test_task_filter_by_priority(self, client, user, task):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('tasks:list') + '?priority=medium')
        assert response.status_code == 200

    def test_user_cannot_access_other_task(self, client, user, user2, task):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('tasks:detail', args=[task.pk]))
        assert response.status_code == 404
