import pytest
from django.test import Client
from django.urls import reverse
from apps.notifications.models import Notification


@pytest.mark.django_db
class TestNotifications:
    def test_notification_list(self, client, user):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('notifications:list'))
        assert response.status_code == 200

    def test_notification_create_and_read(self, client, user):
        client.login(username='testuser', password='testpass123')
        n = Notification.objects.create(
            user=user, title='Test', message='Test msg', notification_type='info'
        )
        assert n.is_read is False
        response = client.get(reverse('notifications:mark_read', args=[n.pk]))
        assert response.status_code == 302
        n.refresh_from_db()
        assert n.is_read is True

    def test_mark_all_read(self, client, user):
        client.login(username='testuser', password='testpass123')
        Notification.objects.create(user=user, title='N1', message='M1')
        Notification.objects.create(user=user, title='N2', message='M2')
        response = client.post(reverse('notifications:mark_all_read'))
        assert response.status_code == 302
        assert user.notifications.filter(is_read=False).count() == 0
