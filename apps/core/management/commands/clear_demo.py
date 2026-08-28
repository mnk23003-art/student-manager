from django.core.management.base import BaseCommand
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Clear all demo data'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='demo')
            user.delete()
            self.stdout.write(self.style.SUCCESS('Demo data cleared!'))
        except User.DoesNotExist:
            self.stdout.write('No demo user found.')
