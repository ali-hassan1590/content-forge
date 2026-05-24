from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create a demo user (demo / demo1234) and fix site name for allauth."

    def handle(self, *args, **options):
        Site.objects.update_or_create(
            pk=1,
            defaults={"domain": "localhost:8000", "name": "ContentForge"},
        )

        if User.objects.filter(username="demo").exists():
            self.stdout.write(self.style.WARNING("Demo user already exists (demo / demo1234)"))
            return

        User.objects.create_user(
            username="demo",
            email="demo@contentforge.local",
            password="demo1234",
        )
        self.stdout.write(self.style.SUCCESS("Demo user created: username=demo  password=demo1234"))
