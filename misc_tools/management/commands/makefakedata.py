from random import choice, randint

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from bands import models


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **options):
        sow = self.stdout.write

        # Groups
        # ========================================
        groups_to_make = [
            'band_manager',
            'booking_manager',
            'chief_booking_manager',
            'technical_staff',
            'audio_technician',
            'light_technician',
        ]

        existing_groups = Group.objects.all()

        for group in groups_to_make:
            if existing_groups.filter(name=group).exists():
                sow(f'{group} exists')
            else:
                sow(f'{group} does not exist -- creating')
                Group.objects.create(name=group)

        # Users
        # ========================================
        password = 'qweqweqwe'
        all_users = User.objects.all()
        # Admin
        try:
            admin_user = User.objects.create_superuser('admin', '', password)
        except IntegrityError:
            sow('user already exists')

        # Technical staff
        general_group = Group.objects.get(name='technical_staff')
        for i in range(20):
            for tech_type in ['light_technician', 'audio_technician']:
                name = f'{tech_type}_{i}'
                if not User.objects.filter(username=name).exists():
                    user = User.objects.create_user(name, '', password)
                    specific_group = Group.objects.get(name=tech_type)
                    specific_group.user_set.add(user)
                    general_group.user_set.add(user)
                else:
                    sow(f"{name} already exists")

        # Stages
        # ========================================
        stage_names = [
            "here", "hick", "high", "hind", "hoar", "holy", "home", "homy",
            "hued", "huge", "hung", "hush", "iced", "icky", "idle", "iffy",
            "ilka", "iron", "jake", "jerk", "jive", "junk", "jury", "just",
            "keen", "kind", "king", "lacy", "laic", "lame", "lang", "lank",
            "last", "late", "lazy", "lead", "lean", "left", "less", "levo",
            "lewd", "lief", "life", "like", "limp", "lite", "live", "loco",
            "logy", "lone",
        ]
        stage_sizes = models.Stage.STAGE_SIZE_CHOICES
        for name in stage_names:
            name = name.capitalize()
            if not models.Stage.objects.filter(name=name).exists():
                try:
                    models.Stage.objects.create(
                        name=f'{name}',
                        num_seats=randint(1,10)*100,
                        stage_size=choice(stage_sizes)
                    )
                except IntegrityError:
                    sow("couldn't create stage")
            else:
                sow(f'Stage {name} already exists')

        # Genres
        # ========================================
        genres = ['Pop', 'Gangster rap']
        for genre in genres:
            if not models.Genre.objects.filter(name=genre).exists():
                try:
                    models.Genre.objects.create(name=genre)
                except:
                    sow(f"couldn't create genre {genre}")

        # Bands
        # ========================================
        band_names = [
            "Adam and the Ants", "Add N to (X)", "Adele", "The Adverts",
            "Akercocke", "Alabama 3", "The Alan Parsons Project",
            "Alien Sex Fiend", "All Saints", "AlunaGeorge", "Amy Winehouse",
            "Angel Witch", "The Apostles", "Archive", "Athlete", "Babyshambles",
            "Bad Company", "Basement Jaxx", "Bastille", "Bat For Lashes",
            "Benga", "Ben Howard", "Big Bang", "The Big Pink", "Billy Idol",
            "Blancmange", "Bleech", "Bloc Party", "Blues Incorporated",
            "The Bluetones", "The Bolshoi", "Bombay Bicycle Club",
            "Bonzo Dog Doo-Dah Band", "Bow Wow Wow", "Bush", "Busted",
            "Callender's Cableworks Band",
            "Carter The Unstoppable Sex Machine", "Chad & Jeremy",
            "Chase & Status", "Chris Farlowe and the Thunderbirds",
            "The Chords", "The Clash", "Classix Nouveaux",
            "Clement Marfo & The Frontline", "Client", "Coldplay", "Cream",
            "The Creatures", "Crystal Fighters", "Culture Club", "The Damned",
            "Darkstar", "Daughter", "David Bowie", "The Dave Clark Five",
            "Days in december", "Death in Vegas", "Deep Purple", "The Defiled",
            "Delilah", "Devil Sold His Soul", "Dirty Pretty Things",
            "Dizzee Rascal", "Django Django", "DragonForce", "Dry the River",
            "Dot Rotten", "Dumpy's Rusty Nuts", "Dusty Springfield",
            "Ebony Bones", "The Edge", "Eliza Doolittle", "Ella Mai",
            "Engineers", "Erasure", "Eurythmics", "Example", "The Faces",
        ]
        legal_characters = 'abcdefghijklmnopqrstuvwxyz_'
        for band_name in band_names:
            Band = models.Band
            if not Band.objects.filter(name=band_name).exists():
                manager_name = band_name.lower()
                new_manager_name = ''
                for (i,c) in enumerate(manager_name):
                    if c in legal_characters:
                        new_manager_name += c
                    else:
                        new_manager_name += '_'
                new_manager_name += '_manager'
                sow(f'{new_manager_name}')

                manager = User.objects.create_user(new_manager_name, '', password)
                Band.objects.create(name=band_name, manager=manager,
                                    genre=choice(models.Genre.objects.all()))

        # Concerts
        # ========================================
        Concert = models.Concert
        taglines = [' - A New Hope', ' Strike Back', '']
        for band in models.Band.objects.all():
            sow(f"{band}")

        # Festivals
        # ========================================
