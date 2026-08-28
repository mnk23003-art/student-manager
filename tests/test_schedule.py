import pytest
from django.test import Client
from django.urls import reverse
from apps.schedule.models import ScheduleItem
from apps.subjects.models import Subject
from datetime import time


@pytest.mark.django_db
class TestSchedule:
    def test_schedule_view(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('schedule:view'))
        assert response.status_code == 200

    def test_schedule_create(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'subject': subject.pk,
            'day_of_week': 0,
            'start_time': '09:00',
            'end_time': '10:30',
            'lesson_type': 'lecture',
            'teacher': 'Dr. Smith',
            'room': 'Room 101',
            'notes': '',
        }
        response = client.post(reverse('schedule:create'), data)
        assert response.status_code == 302
        assert ScheduleItem.objects.filter(subject=subject).exists()

    def test_schedule_conflict_detection(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        ScheduleItem.objects.create(
            user=user, subject=subject, semester=semester,
            day_of_week=0, start_time=time(9, 0), end_time=time(11, 0),
            lesson_type='lecture'
        )
        subject2 = Subject.objects.create(
            user=user, semester=semester, name='Physics', color='#10B981'
        )
        data = {
            'subject': subject2.pk,
            'day_of_week': 0,
            'start_time': '10:00',
            'end_time': '12:00',
            'lesson_type': 'seminar',
            'teacher': '',
            'room': '',
            'notes': '',
        }
        response = client.post(reverse('schedule:create'), data)
        assert response.status_code == 200

    def test_schedule_delete(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        item = ScheduleItem.objects.create(
            user=user, subject=subject, semester=semester,
            day_of_week=0, start_time=time(9, 0), end_time=time(10, 30),
            lesson_type='lecture'
        )
        response = client.post(reverse('schedule:delete', args=[item.pk]))
        assert response.status_code == 302
        assert not ScheduleItem.objects.filter(pk=item.pk).exists()
