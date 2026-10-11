
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Ensure the configured Django administrator account exists."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not username or not password:
            raise CommandError(
                "DJANGO_SUPERUSER_USERNAME and "
                "DJANGO_SUPERUSER_PASSWORD must be configured."
            )

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Administrator account '{username}' created."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Administrator account '{username}' verified and updated."
                )
            )
