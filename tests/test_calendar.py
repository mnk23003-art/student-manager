import pytest
from django.test import Client
from django.urls import reverse
from apps.calendar.models import CalendarEvent
from datetime import date, timedelta


@pytest.mark.django_db
class TestCalendar:
    def test_calendar_view(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('calendar:view'))
        assert response.status_code == 200

    def test_event_create(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Event',
            'description': '',
            'date': date.today().isoformat(),
            'start_time': '',
            'end_time': '',
            'event_type': 'event',
            'color': '#3B82F6',
        }
        response = client.post(reverse('calendar:event_create'), data)
        assert response.status_code == 302
        assert CalendarEvent.objects.filter(title='New Event').exists()

    def test_event_delete(self, client, user, semester):
        client.login(username='testuser', password='testpass123')
        event = CalendarEvent.objects.create(
            user=user, semester=semester, title='Test Event',
            date=date.today(), event_type='event'
        )
        response = client.post(reverse('calendar:event_delete', args=[event.pk]))
        assert response.status_code == 302
        assert not CalendarEvent.objects.filter(pk=event.pk).exists()
