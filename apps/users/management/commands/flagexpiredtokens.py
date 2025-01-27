from django.utils import timezone
from datetime import timedelta
from apps.users.models import UserConfirmationToken
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Flag tokens as outdated when they expire"

    def handle(self, *args, **options):
        # diff = timezone.now() - timedelta(seconds=30)
        diff = timezone.now() - timedelta(minutes=5)
        count = UserConfirmationToken.objects.filter(date_created__lt=diff, is_used=False).update(is_used=True)
        print(f"Flagged {count} tokens as outdated.")
