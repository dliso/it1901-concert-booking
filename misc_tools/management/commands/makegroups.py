from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the groups needed by the application'

    def handle(self, *args, **options):
        sow = self.stdout.write

        groups_to_make = [
            'Band Manager',
            'Booking Manager',
            'Booking Deputy',
        ]

        existing_groups = Group.objects.all()

        for group in groups_to_make:
            if existing_groups.filter(name=group).exists():
                sow(f'{group} exists')
            else:
                sow(f'{group} does not exist -- creating')
                Group.objects.create(name=group)
