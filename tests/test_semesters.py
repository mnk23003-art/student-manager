import pytest
from django.test import Client
from django.urls import reverse
from apps.semesters.models import Semester
from datetime import date, timedelta


@pytest.mark.django_db
class TestSemesters:
    def test_semester_list(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('semesters:list'))
        assert response.status_code == 200

    def test_semester_create(self, client, user):
        client.login(username='testuser', password='testpass123')
        data = {
            'name': 'New Semester',
            'academic_year': '2026/2027',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=120),
        }
        response = client.post(reverse('semesters:create'), data)
        assert response.status_code == 302
        assert Semester.objects.filter(name='New Semester').exists()

    def test_semester_update(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Updated Semester',
            'academic_year': '2026/2027',
            'start_date': semester.start_date,
            'end_date': semester.end_date,
        }
        response = client.post(reverse('semesters:update', args=[semester.pk]), data)
        assert response.status_code == 302
        semester.refresh_from_db()
        assert semester.name == 'Updated Semester'

    def test_semester_delete(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('semesters:delete', args=[semester.pk]))
        assert response.status_code == 302
        assert not Semester.objects.filter(pk=semester.pk).exists()

    def test_set_active(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        sem2 = Semester.objects.create(
            user=user, name='Sem 2', academic_year='2026/2027',
            start_date=date.today(), end_date=date.today() + timedelta(days=120)
        )
        response = client.get(reverse('semesters:set_active', args=[sem2.pk]))
        assert response.status_code == 302
        sem2.refresh_from_db()
        semester.refresh_from_db()
        assert sem2.is_active is True
        assert semester.is_active is False

    def test_user_cannot_access_other_semester(self, client, user, user2):
        client.login(username='user2', password='pass1234')
        sem = Semester.objects.create(
            user=user, name='User1Sem', academic_year='2026/2027',
            start_date=date.today(), end_date=date.today() + timedelta(days=120)
        )
        response = client.post(reverse('semesters:delete', args=[sem.pk]))
        assert Semester.objects.filter(pk=sem.pk).exists()
