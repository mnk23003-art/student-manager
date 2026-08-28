import pytest
from django.test import Client
from django.urls import reverse
from apps.goals.models import Goal


@pytest.mark.django_db
class TestGoals:
    def test_goal_list(self, client, user, goal):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('goals:list'))
        assert response.status_code == 200

    def test_goal_create(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Goal',
            'description': '',
            'target': 'Target',
            'progress': 0,
            'deadline': '',
            'status': 'not_started',
        }
        response = client.post(reverse('goals:create'), data)
        assert response.status_code == 302
        assert Goal.objects.filter(title='New Goal').exists()

    def test_goal_detail(self, client, user, goal):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('goals:detail', args=[goal.pk]))
        assert response.status_code == 200

    def test_goal_delete(self, client, user, goal):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('goals:delete', args=[goal.pk]))
        assert response.status_code == 302
        assert not Goal.objects.filter(pk=goal.pk).exists()
