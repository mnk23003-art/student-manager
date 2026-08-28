import pytest
from django.test import Client
from django.urls import reverse
from apps.accounts.models import User, StudentProfile, UserSettings


@pytest.mark.django_db
class TestRegistration:
    def test_register_get(self, client):
        response = client.get(reverse('accounts:register'))
        assert response.status_code == 200

    def test_register_post(self, client):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = client.post(reverse('accounts:register'), data)
        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()
        assert StudentProfile.objects.filter(user__username='newuser').exists()
        assert UserSettings.objects.filter(user__username='newuser').exists()


@pytest.mark.django_db
class TestLogin:
    def test_login_get(self, client):
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200

    def test_login_post(self, client, user):
        response = client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 302

    def test_login_wrong_password(self, client, user):
        response = client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200


@pytest.mark.django_db
class TestLogout:
    def test_logout(self, client, user):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('accounts:logout'))
        assert response.status_code == 302


@pytest.mark.django_db
class TestProfile:
    def test_profile_view(self, client, user):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 200

    def test_profile_update(self, client, user):
        client.login(username='testuser', password='testpass123')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'university': 'New Uni',
            'faculty': 'New Faculty',
            'specialization': '',
            'course': '',
            'academic_year': '',
            'phone': '',
        }
        response = client.post(reverse('accounts:profile'), data)
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.first_name == 'Updated'


@pytest.mark.django_db
class TestUserIsolation:
    def test_user_cannot_see_other_profile(self, client, user, user2):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 200
