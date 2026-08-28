import pytest
from django.test import Client
from django.urls import reverse
from apps.exams.models import Exam
from datetime import date, time, timedelta


@pytest.mark.django_db
class TestExams:
    def test_exam_list(self, client, user, exam):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('exams:list'))
        assert response.status_code == 200

    def test_exam_create(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'subject': subject.pk,
            'title': 'Midterm',
            'date': (date.today() + timedelta(days=14)).isoformat(),
            'time': '10:00',
            'location': 'Room 301',
            'description': '',
            'notes': '',
        }
        response = client.post(reverse('exams:create'), data)
        assert response.status_code == 302
        assert Exam.objects.filter(title='Midterm').exists()

    def test_exam_detail(self, client, user, exam):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('exams:detail', args=[exam.pk]))
        assert response.status_code == 200

    def test_exam_delete(self, client, user, exam):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('exams:delete', args=[exam.pk]))
        assert response.status_code == 302
        assert not Exam.objects.filter(pk=exam.pk).exists()

    def test_exam_days_until(self, user, semester, subject):
        exam = Exam.objects.create(
            user=user, semester=semester, subject=subject,
            title='Future Exam', date=date.today() + timedelta(days=5)
        )
        assert exam.days_until() == 5

    def test_exam_is_upcoming(self, user, semester, subject):
        exam = Exam.objects.create(
            user=user, semester=semester, subject=subject,
            title='Future Exam', date=date.today() + timedelta(days=5)
        )
        assert exam.is_upcoming() is True

    def test_exam_is_past(self, user, semester, subject):
        exam = Exam.objects.create(
            user=user, semester=semester, subject=subject,
            title='Past Exam', date=date.today() - timedelta(days=5)
        )
        assert exam.is_past() is True

    def test_user_cannot_access_other_exam(self, client, user, user2, exam):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('exams:detail', args=[exam.pk]))
        assert response.status_code == 404
