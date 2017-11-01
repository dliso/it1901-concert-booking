from django.contrib.auth.models import Group
from rules import add_perm, always_allow, always_deny, is_superuser, predicate

from . import models
from .groups import Groups


@predicate
def is_manager(user, tech_need):
    if not tech_need:
        return False
    return user == tech_need.concert_name.band_name.manager


@predicate
def is_concert_booker(user):
    return user.groups.filter(name=Groups.CONCERT_BOOKERS.value).exists()


@predicate
def is_chief_booker(user):
    return user.groups.filter(name=Groups.CHIEF_BOOKERS.value).exists()


add_perm('bands', always_allow)
# add_perm('bands.add_technicalneed', is_superuser | is_manager)
add_perm('bands.change_technicalneed', is_superuser | is_manager)
# add_perm('bands.delete_technicalneed', is_superuser | is_manager)

add_perm('stage.view_econ_report', is_concert_booker | is_chief_booker)

add_perm('concert.edit', is_concert_booker | is_chief_booker)
add_perm('concert.edit_tech_staff', is_concert_booker | is_chief_booker)
