from random import choice, choices, randint

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

from bands import groups, models
from bands.groups import Groups


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **options):
        sow = self.stdout.write

        groups_to_make = [g.value for g in groups.Groups]

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
        sow('--- creating admin')
        try:
            admin_user = User.objects.create_superuser('admin', '', password)
        except IntegrityError:
            sow('user already exists')

        # Technical staff
        sow('--- creating tech staff')
        # general_group = Group.objects.get(name='technical_staff')
        for i in range(20):
            for tech_type in [Groups.LIGHT_TECHS.value, Groups.AUDIO_TECHS.value]:
                name = f'{tech_type}_{i}'
                if not User.objects.filter(username=name).exists():
                    user = User.objects.create_user(name, '', password)
                    specific_group = Group.objects.get(name=tech_type)
                    specific_group.user_set.add(user)
                    # general_group.user_set.add(user)
                else:
                    sow(f"{name} already exists")

        # PR managers
        sow('--- creating PR managers')
        pr_group = Group.objects.get(name=Groups.PR_MANAGERS.value)
        for i in range(5):
            name = f'pr_manager_{i}'
            if not User.objects.filter(username=name).exists():
                user = User.objects.create_user(name, '', password)
                pr_group.user_set.add(user)
            else:
                sow(f"{name} already exists")

        # Stages
        # ========================================
        sow('--- creating stages')
        models.Stage.objects.all().delete()
        stage_names = [
            "here", "hick", "high", "hind", "hoar", "holy", "home", "homy",
            "cake", "butter", "orange", "panda", "pudding", "snake"
        ]
        stage_sizes = models.Stage.STAGE_SIZE_CHOICES
        for name in stage_names:
            name = name.capitalize() + ' Stage'
            if not models.Stage.objects.filter(name=name).exists():
                try:
                    models.Stage.objects.create(
                        name=f'{name}',
                        num_seats=randint(1,10)*100,
                        stage_size=choice(stage_sizes)[0]
                    )
                except IntegrityError:
                    sow("couldn't create stage")
            else:
                sow(f'Stage {name} already exists')

        # Genres
        # ========================================
        sow('--- creating genres')
        genres = ['Pop', 'Gangster rap']
        for genre in genres:
            if not models.Genre.objects.filter(name=genre).exists():
                try:
                    models.Genre.objects.create(name=genre)
                except:
                    sow(f"couldn't create genre {genre}")

        # Bands
        # ========================================
        sow('--- creating bands')
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

                if User.objects.filter(username=new_manager_name).exists():
                    manager = User.objects.get(username=new_manager_name)
                else:
                    manager = User.objects.create_user(new_manager_name, '', password)
                Band.objects.create(name=band_name, manager=manager,
                                    genre=choice(models.Genre.objects.all()))

        # Concerts
        # ========================================
        sow('--- creating concerts')
        Concert = models.Concert
        Concert.objects.all().delete()
        models.TechnicalNeed.objects.all().delete()
        taglines = [' - A New Hope', ' Strike Back', ' Return', ' II', ' III', ' IV']
        times = []
        now = timezone.now()
        year = now.year
        years = list(range(year - 5, year + 2))
        months = [(now.month + i) % 12 for i in range(1)]
        days = [(now.day + i) % 28 for i in range(-5, 6)]
        hours = [16, 18, 20, 22]
        for year in years:
            times.append(now.replace(year=year))
        stages = models.Stage.objects.all()
        genres = models.Genre.objects.all()
        light_techs = Group.objects.get(name=Groups.LIGHT_TECHS.value).user_set.all()
        audio_techs = Group.objects.get(name=Groups.AUDIO_TECHS.value).user_set.all()

        # Requirements
        audio_reqs = ['speakers', 'microphones', 'monitors', 'guitars',
                      'keyboards']
        light_reqs = ['spotlights', 'red lights', 'green lights',
                      'blue lights', 'yellow lights']
        other_reqs = ['water bottles', 'pink mentos']

        for band in models.Band.objects.all():
            sow(f"{band}")
            for _ in range(randint(0,5)):
                tagline = choice(taglines)
                concert = Concert.objects.create(
                    name=f'{band.name} {tagline}',
                    band_name=band,
                    stage_name=choice(stages),
                    genre_music=choice(genres),
                    concert_time=timezone.datetime(
                        choice(years),
                        choice(months),
                        choice(days),
                        choice(hours),
                    ),
                    ticket_price=randint(100,1000),
                )
                concert.light_tech = choices(light_techs, k=randint(1,5))
                concert.sound_tech = choices(audio_techs, k=randint(1,5))
                concert.save()
                # Make technical requirements
                sound = ''
                for req in choices(audio_reqs, k=randint(0, len(audio_reqs) + 1)):
                    sound += f'- {randint(1,10)} {req}\n'
                light = ''
                for req in choices(light_reqs, k=randint(0, len(light_reqs) + 1)):
                    light += f'- {randint(1,10)} {req}\n'
                other = ''
                for req in choices(other_reqs, k=randint(0, len(other_reqs) + 1)):
                    other += f'- {randint(1,10)} {req}\n'
                tech_req = models.TechnicalNeed.objects.create(
                    concert_name=concert,
                    sound=sound,
                    light=light,
                    other_technical_needs=other
                )

        # Festivals
        # ========================================
        Festival = models.Festival
        Festival.objects.all().delete()
        names = ['Testivalen']
        for year in years:
            for name in names:
                full_name = f'{name} {year}'
                if not Festival.objects.filter(name=full_name).exists():
                    festival = Festival.objects.create(name=full_name)
                    festival.concerts = Concert.objects.filter(concert_time__year=year)
                    festival.save()
