import pytest
from django.test import Client
from django.urls import reverse
from apps.subjects.models import Subject


@pytest.mark.django_db
class TestSubjects:
    def test_subject_list(self, client, user, subject):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('subjects:list'))
        assert response.status_code == 200

    def test_subject_create(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Physics',
            'teacher': 'Dr. Jones',
            'room': 'Lab 101',
            'credits': 3,
            'hours': 45,
            'color': '#10B981',
            'description': '',
        }
        response = client.post(reverse('subjects:create'), data)
        assert response.status_code == 302
        assert Subject.objects.filter(name='Physics').exists()

    def test_subject_detail(self, client, user, subject):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('subjects:detail', args=[subject.pk]))
        assert response.status_code == 200

    def test_subject_update(self, client, user, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Updated Math',
            'teacher': 'Dr. Smith',
            'room': 'Room 102',
            'credits': 4,
            'hours': 60,
            'color': '#3B82F6',
            'description': '',
        }
        response = client.post(reverse('subjects:update', args=[subject.pk]), data)
        assert response.status_code == 302
        subject.refresh_from_db()
        assert subject.name == 'Updated Math'

    def test_subject_delete(self, client, user, subject):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('subjects:delete', args=[subject.pk]))
        assert response.status_code == 302
        assert not Subject.objects.filter(pk=subject.pk).exists()

    def test_user_cannot_access_other_subject(self, client, user, user2, subject):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('subjects:detail', args=[subject.pk]))
        assert response.status_code == 404
