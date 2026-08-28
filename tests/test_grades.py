import pytest
from django.test import Client
from django.urls import reverse
from apps.grades.models import Grade
from apps.grades.services import calculate_average_grade, calculate_weighted_average, calculate_gpa
from datetime import date


@pytest.mark.django_db
class TestGrades:
    def test_grade_list(self, client, user, grade):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('grades:list'))
        assert response.status_code == 200

    def test_grade_create(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'subject': subject.pk,
            'title': 'Quiz 1',
            'grade_type': 'quiz',
            'score': 90,
            'max_score': 100,
            'weight': 15,
            'date': date.today().isoformat(),
            'comment': '',
        }
        response = client.post(reverse('grades:create'), data)
        assert response.status_code == 302
        assert Grade.objects.filter(title='Quiz 1').exists()

    def test_grade_delete(self, client, user, grade):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('grades:delete', args=[grade.pk]))
        assert response.status_code == 302
        assert not Grade.objects.filter(pk=grade.pk).exists()

    def test_grade_get_percentage(self, user, semester, subject):
        grade = Grade.objects.create(
            user=user, semester=semester, subject=subject,
            title='Test', score=85, max_score=100
        )
        assert grade.get_percentage() == 85.0

    def test_grade_gpa_4(self, user, semester, subject):
        grade = Grade.objects.create(
            user=user, semester=semester, subject=subject,
            title='Test', score=95, max_score=100
        )
        assert grade.get_gpa_4() == 4.0

    def test_grade_5_point(self, user, semester, subject):
        grade = Grade.objects.create(
            user=user, semester=semester, subject=subject,
            title='Test', score=95, max_score=100
        )
        assert grade.get_5_point() == 5

    def test_grade_10_point(self, user, semester, subject):
        grade = Grade.objects.create(
            user=user, semester=semester, subject=subject,
            title='Test', score=95, max_score=100
        )
        assert grade.get_10_point() == 10


@pytest.mark.django_db
class TestGradeServices:
    def test_calculate_average(self, user, semester, subject):
        Grade.objects.create(user=user, semester=semester, subject=subject, title='G1', score=80, max_score=100)
        Grade.objects.create(user=user, semester=semester, subject=subject, title='G2', score=90, max_score=100)
        avg = calculate_average_grade(user, semester)
        assert avg == 85.0

    def test_calculate_average_empty(self, user, semester):
        avg = calculate_average_grade(user, semester)
        assert avg is None

    def test_calculate_weighted_average(self, user, semester, subject):
        Grade.objects.create(user=user, semester=semester, subject=subject, title='G1', score=80, max_score=100, weight=20)
        Grade.objects.create(user=user, semester=semester, subject=subject, title='G2', score=90, max_score=100, weight=30)
        avg = calculate_weighted_average(user, semester)
        assert avg is not None

    def test_grade_score_exceeds_max_fails(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'subject': subject.pk,
            'title': 'Bad Grade',
            'grade_type': 'test',
            'score': 150,
            'max_score': 100,
            'weight': 10,
            'date': date.today().isoformat(),
            'comment': '',
        }
        response = client.post(reverse('grades:create'), data)
        assert response.status_code == 200

    def test_user_cannot_see_other_grades(self, client, user, user2, grade):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('grades:list'))
        assert grade not in response.context['grades']
