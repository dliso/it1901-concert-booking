from random import choice, choices, randrange

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Create a bunch of randomly named users with random group affiliations for
    testing purposes.
    """
    help = 'Create test users and assign them to groups'

    def handle(self, *args, **options):
        sow = self.stdout.write
        first_names = [
            "about", "above", "abuzz", "acute", "adult", "adust", "agile",
            "alien", "alike", "alive", "alone", "aloof", "amino", "amiss",
            "amuck", "anile", "apian", "apish", "avian", "axial", "axile",
            "azoic", "beige", "blind", "blond", "bloop", "blown", "blowy",
            "bluff", "blunt", "boomy", "bound", "brief", "briny", "brisk",
            "broad", "broke", "brood", "brown", "brute", "built", "chief",
            "chill", "choky", "close", "cloze", "couth", "crisp", "crook",
            "above", "abuzz", "acute", "adult", "adust", "agile", "alien",
            "alike", "alive", "alone", "aloof", "amino", "amiss", "amuck",
            "anile", "apian", "apish", "avian", "axial", "axile", "azoic",
            "beige", "blind", "blond", "bloop", "blown", "blowy", "bluff",
            "blunt", "boomy", "bound", "brief", "briny", "brisk", "broad",
            "broke", "brood", "brown", "brute", "built", "cross", "crude",
            "cruel", "daily", "dairy", "drier", "droll", "drunk", "dying",
            "ebony", "equal", "erose", "faint", "flown", "fluid", "fluky",
            "flush", "fried", "front", "frore", "gaudy", "gaunt", "gauzy",
            "going", "gooey", "goofy", "goosy", "grimy", "gross", "group",
            "grown", "gruff", "hairy", "haute", "hyoid", "iliac", "imido",
            "imino", "ivied", "ivory", "joint", "juicy", "known", "kooky",
            "loony", "loopy", "loose", "loury", "lousy", "loyal", "lying",
            "moire", "moist", "moody", "moony", "mousy", "naive", "noisy",
            "ovine", "ovoid", "owing", "phony", "pious", "plumb", "plump",
            "plumy", "plush", "pricy", "prime", "primo", "print", "prior",
            "privy", "prize", "prone", "proof", "prosy", "proud", "pyoid",
            "quick", "quiet", "quits", "rainy", "roily", "rooky", "roomy",
            "rooty", "rough", "round", "royal", "saucy", "shier", "shiny",
            "shoal", "short", "showy", "skimp", "skyey", "slick", "slier",
            "slimy", "slink", "smoky", "snide", "snowy", "sooth", "sooty",
            "sound", "soupy", "south", "spicy", "spiky", "spiny", "sport",
            "squab", "squat", "stiff", "still", "stock", "stone", "stony",
            "stoss", "stout", "swift", "swing", "swish", "sworn", "taunt",
            "teiid", "thick", "thine", "think", "tough", "trial", "trick",
            "tried", "trine", "trite", "union", "usual", "utile", "veiny",
            "weird", "which", "white", "whole", "whose", "woody", "wooly",
            "woozy", "wrier", "wrong", "wroth", "young",
        ]

        last_names = [
            "abohm", "abysm", "abyss", "acorn", "adobe", "adobo", "aging",
            "agism", "agita", "agony", "agora", "ahold", "aioli", "aloin",
            "alula", "amice", "amide", "amigo", "amine", "amity", "amole",
            "amour", "anima", "anime", "anion", "anode", "anole", "aquae",
            "aroid", "aroma", "atoll", "atomy", "atony", "axiom", "axion",
            "azide", "azine", "azole", "azote", "azoth", "azure", "bairn",
            "baisa", "baize", "bayou", "biome", "biota", "blini", "bliss",
            "bloke", "coign", "cooky", "coupe", "coypu", "crier", "crime",
            "croci", "croft", "crone", "crony", "croup", "croze", "cruet",
            "crura", "cruse", "crypt", "cuish", "daisy", "deism", "deity",
            "dhole", "dhoti", "diode", "doily", "doing", "doozy", "dough",
            "doula", "doura", "doyen", "droit", "dross", "druid", "drupe",
            "druse", "dryad", "dryer", "duomo", "edict", "elite", "enoki",
            "epoch", "epode", "etude", "etyma", "exine", "exurb", "fairy",
            "faith", "fauna", "haick", "haiku", "haint", "haole", "haugh",
            "haulm", "hooch", "hooey", "hooky", "houri", "icing", "idiom",
            "idiot", "idyll", "ilium", "imide", "imine", "inion", "irony",
            "joual", "joule", "kaiak", "kauri", "khoum", "kiosk", "klick",
            "kloof", "klutz", "knish", "krill", "krona", "krone", "kroon",
            "laird", "laity", "leone", "loofa", "lough", "loupe", "maize",
            "maund", "mauve", "mayor", "mbira", "moola", "moose", "mould",
            "myoma", "myope", "naiad", "quoit", "quota", "raita", "rayah",
            "rayon", "reins", "rhino", "rhumb", "riyal", "saiga", "sault",
            "sauna", "saury", "scion", "scone", "scuba", "scudo", "scurf",
            "scuta", "scute", "seism", "shire", "shirt", "shiva", "shoat",
            "shogi", "shoji", "shoon", "shote", "shott", "shoyu", "skiff",
            "skill", "skink", "skort", "skosh", "skull", "sloka", "sloop",
            "sloth", "sloyd", "slype", "smith", "smolt", "snoek", "snook",
            "snout", "spica", "spick", "spine",
        ]

        num_users = 10
        groups = Group.objects.all()
        max_num_groups_wanted = 3
        max_num_groups = min(groups.count(), max_num_groups_wanted)
        password = 'qweqweqwe'
        for _ in range(num_users):
            first_name = choice(first_names)
            last_name = choice(last_names)
            username = f'{first_name}_{last_name}'
            if not User.objects.filter(username=username).exists():
                # Create user
                user = User.objects.create_user(
                    username=username, password=password)
                user.first_name = first_name.title()
                user.last_name = last_name.title()
                user.save()
                # Add user to groups
                num_groups = randrange(1, max_num_groups)
                chosen_groups = choices(groups, k=num_groups)
                for g in chosen_groups:
                    user.groups.add(g)
