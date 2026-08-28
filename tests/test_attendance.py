import pytest
from django.test import Client
from django.urls import reverse
from apps.attendance.models import Attendance
from apps.attendance.services import calculate_attendance_stats
from datetime import date, timedelta


@pytest.mark.django_db
class TestAttendance:
    def test_attendance_list(self, client, user, attendance):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('attendance:list'))
        assert response.status_code == 200

    def test_attendance_create(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'subject': subject.pk,
            'date': date.today().isoformat(),
            'status': 'present',
            'notes': '',
        }
        response = client.post(reverse('attendance:create'), data)
        assert response.status_code == 302
        assert Attendance.objects.filter(subject=subject, date=date.today()).exists()

    def test_attendance_update(self, client, user, attendance):
        client.login(username='testuser', password='testpass123')
        data = {
            'subject': attendance.subject.pk,
            'date': attendance.date.isoformat(),
            'status': 'absent',
            'notes': '',
        }
        response = client.post(reverse('attendance:update', args=[attendance.pk]), data)
        assert response.status_code == 302
        attendance.refresh_from_db()
        assert attendance.status == 'absent'

    def test_attendance_delete(self, client, user, attendance):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('attendance:delete', args=[attendance.pk]))
        assert response.status_code == 302
        assert not Attendance.objects.filter(pk=attendance.pk).exists()


@pytest.mark.django_db
class TestAttendanceServices:
    def test_calculate_stats(self, user, semester, subject):
        for i in range(10):
            Attendance.objects.create(
                user=user, semester=semester, subject=subject,
                date=date.today() - timedelta(days=i),
                status='present' if i < 8 else 'absent'
            )
        stats = calculate_attendance_stats(user, semester)
        assert stats is not None
        assert stats['total'] == 10
        assert stats['percentage'] == 80.0

    def test_calculate_stats_empty(self, user, semester):
        stats = calculate_attendance_stats(user, semester)
        assert stats is None
