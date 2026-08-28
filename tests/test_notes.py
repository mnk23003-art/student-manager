import pytest
from django.test import Client
from django.urls import reverse
from apps.notes.models import Note


@pytest.mark.django_db
class TestNotes:
    def test_note_list(self, client, user, note):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('notes:list'))
        assert response.status_code == 200

    def test_note_create(self, client, user, semester, subject):
        client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Note',
            'content': 'Content here',
            'subject': subject.pk,
            'tags': 'test,note',
        }
        response = client.post(reverse('notes:create'), data)
        assert response.status_code == 302
        assert Note.objects.filter(title='New Note').exists()

    def test_note_detail(self, client, user, note):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('notes:detail', args=[note.pk]))
        assert response.status_code == 200

    def test_note_delete(self, client, user, note):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('notes:delete', args=[note.pk]))
        assert response.status_code == 302
        assert not Note.objects.filter(pk=note.pk).exists()

    def test_note_search(self, client, user, note):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('notes:list') + '?q=Test')
        assert response.status_code == 200

    def test_note_get_tags_list(self, user, note):
        tags = note.get_tags_list()
        assert 'test' in tags
        assert 'notes' in tags

    def test_user_cannot_access_other_note(self, client, user, user2, note):
        client.login(username='user2', password='pass1234')
        response = client.get(reverse('notes:detail', args=[note.pk]))
        assert response.status_code == 404
